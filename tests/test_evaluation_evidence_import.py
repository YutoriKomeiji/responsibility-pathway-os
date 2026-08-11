# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
from pathlib import Path

from rpos import OperationDefinition, OperationState, RposService
from rpos.cli import run


def _create_gated_operation(database: Path) -> None:
    service = RposService(str(database))
    service.propose(
        OperationDefinition(
            operation_id="import-001",
            action_name="bounded_external_operation",
            requested_by="requester",
            execution_actor="executor",
            approval_authority="human_authority",
            human_return_point="human-authority-review",
            residual_owner="operator",
            resume_authority="human_authority",
            requires_human_gate=True,
            verification_required=True,
        )
    )


def _valid_payload() -> dict[str, object]:
    return {
        "evidence_id": "safety-eval-001",
        "evidence_class": "safety_evaluation",
        "source_system": "external-safety-evaluator",
        "source_reference": "evaluation-run-001",
        "source_revision": "rev-2026-08-09",
        "evaluation_scope": "bounded safety evaluation profile",
        "result_summary": "evaluation outputs retained for responsible review",
        "artifact_digest": "test-digest-placeholder",
    }


def test_cli_import_records_strict_provenance_without_state_promotion(tmp_path: Path, capsys) -> None:
    database = tmp_path / "rpos.db"
    _create_gated_operation(database)
    payload_path = tmp_path / "evidence.json"
    payload_path.write_text(json.dumps(_valid_payload()), encoding="utf-8")

    assert run([
        "--db",
        str(database),
        "record-evaluation-json",
        "import-001",
        str(payload_path),
        "--actor",
        "evidence_producer",
    ]) == 0
    capsys.readouterr()

    service = RposService(str(database))
    assert service.inspect("import-001").state is OperationState.HUMAN_GATE
    recorded = [
        event
        for event in service.event_history("import-001")
        if event["event_type"] == "external_evaluation_evidence_recorded"
    ]
    assert len(recorded) == 1
    evidence = recorded[0]["payload"]["evidence"]
    assert evidence["source_revision"] == "rev-2026-08-09"
    assert evidence["artifact_digest"] == "test-digest-placeholder"


def test_cli_import_rejects_unexpected_fields_without_recording_event(tmp_path: Path, capsys) -> None:
    database = tmp_path / "rpos.db"
    _create_gated_operation(database)
    payload = _valid_payload()
    payload["raw_secret_or_unbounded_payload"] = "must-not-be-ingested"  # pragma: allowlist secret
    payload_path = tmp_path / "invalid-evidence.json"
    payload_path.write_text(json.dumps(payload), encoding="utf-8")

    assert run([
        "--db",
        str(database),
        "record-evaluation-json",
        "import-001",
        str(payload_path),
        "--actor",
        "evidence_producer",
    ]) == 2
    captured = capsys.readouterr()
    error = json.loads(captured.err)
    assert error["error"] == "ValueError"
    assert "unexpected fields" in error["message"]

    service = RposService(str(database))
    assert not any(
        event["event_type"] == "external_evaluation_evidence_recorded"
        for event in service.event_history("import-001")
    )


def test_cli_import_requires_source_revision(tmp_path: Path, capsys) -> None:
    database = tmp_path / "rpos.db"
    _create_gated_operation(database)
    payload = _valid_payload()
    del payload["source_revision"]
    payload_path = tmp_path / "missing-revision.json"
    payload_path.write_text(json.dumps(payload), encoding="utf-8")

    assert run([
        "--db",
        str(database),
        "record-evaluation-json",
        "import-001",
        str(payload_path),
        "--actor",
        "evidence_producer",
    ]) == 2
    captured = capsys.readouterr()
    error = json.loads(captured.err)
    assert "source_revision" in error["message"]
