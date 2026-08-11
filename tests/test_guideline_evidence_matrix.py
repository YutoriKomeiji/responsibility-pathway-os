# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
from pathlib import Path

from rpos import EvaluationEvidenceClass, ExternalEvaluationEvidence, OperationDefinition, RposService
from rpos.cli import run
from rpos.guideline import build_guideline_evidence_matrix


def _service(database: Path) -> RposService:
    service = RposService(str(database))
    service.propose(
        OperationDefinition(
            operation_id="guideline-001",
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
    return service


def test_guideline_matrix_reports_evidence_and_gaps_without_compliance_claim(tmp_path: Path) -> None:
    service = _service(tmp_path / "rpos.db")
    service.record_evaluation_evidence(
        "guideline-001",
        actor="evidence_producer",
        evidence=ExternalEvaluationEvidence(
            evidence_id="evaluation-001",
            evidence_class=EvaluationEvidenceClass.SAFETY_EVALUATION,
            source_system="external-safety-evaluator",
            source_reference="evaluation-run-001",
            source_revision="revision-001",
            evaluation_scope="bounded safety evaluation",
            result_summary="bounded evaluation evidence retained",
        ),
    )

    matrix = build_guideline_evidence_matrix(service, "guideline-001")
    rows = {row["mapping_id"]: row for row in matrix["rows"]}

    assert matrix["schema_version"] == "rpos.guideline-matrix.v0.1"
    assert "not a compliance checklist" in matrix["profile_scope"]
    assert rows["jp-aigb-v1.2-info-001"]["evidence_status"] == "evidence_present"
    assert rows["jp-aigb-v1.2-human-001"]["evidence_status"] == "evidence_present"
    assert rows["jp-aigb-v1.2-monitor-001"]["evidence_status"] == "gap"
    assert "external_effect_readback" in rows["jp-aigb-v1.2-monitor-001"]["missing_evidence_groups"]
    assert "legal_or_regulatory_compliance" in rows["jp-aigb-v1.2-info-001"]["not_proven"]


def test_cli_guideline_matrix_is_read_only(tmp_path: Path, capsys) -> None:
    database = tmp_path / "rpos.db"
    service = _service(database)
    before_count = len(service.event_history("guideline-001"))

    assert run(["--db", str(database), "guideline-matrix", "guideline-001"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["profile"] == "jp-ai-guidelines-for-business-v1.2-partial-engineering-map"

    restarted = RposService(str(database))
    assert len(restarted.event_history("guideline-001")) == before_count
