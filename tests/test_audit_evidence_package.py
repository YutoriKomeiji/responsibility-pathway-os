# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
from pathlib import Path

from rpos import (
    AdapterResult,
    EvaluationEvidenceClass,
    ExternalEvaluationEvidence,
    OperationDefinition,
    OperationState,
    ReceiptStatus,
    RposService,
    build_audit_evidence_package,
)
from rpos.cli import run


class ReceiptOnlyAdapter:
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return AdapterResult(
            receipt_status=ReceiptStatus.SUCCEEDED,
            receipt={"accepted": True},
            readback_verified=None,
            reason="receipt_without_independent_readback",
        )


def _service_with_unresolved_operation(database: Path) -> RposService:
    service = RposService(str(database))
    service.propose(
        OperationDefinition(
            operation_id="audit-001",
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
    service.record_evaluation_evidence(
        "audit-001",
        actor="evidence_producer",
        evidence=ExternalEvaluationEvidence(
            evidence_id="evaluation-001",
            evidence_class=EvaluationEvidenceClass.SAFETY_EVALUATION,
            source_system="external-safety-evaluator",
            source_reference="evaluation-run-001",
            evaluation_scope="bounded safety evaluation profile",
            result_summary="evaluation outputs retained for review",
        ),
    )
    service.approve("audit-001", actor="human_authority")
    result = service.dispatch(
        "audit-001",
        attempt_id="attempt-1",
        idempotency_key="audit-dispatch-1",
        adapter=ReceiptOnlyAdapter(),
    )
    assert result.state is OperationState.EFFECT_UNKNOWN
    return service


def test_audit_package_keeps_evidence_classes_separate(tmp_path: Path) -> None:
    service = _service_with_unresolved_operation(tmp_path / "rpos.db")

    package = build_audit_evidence_package(service, "audit-001")

    assert package["schema_version"] == "rpos.audit.v0.1"
    assert package["current_state"] == "effect_unknown"
    assert package["evidence"]["evaluation"]
    assert package["evidence"]["authority_and_admission"]
    assert package["evidence"]["execution_and_receipt"]
    assert package["evidence"]["external_effect_readback"] == []
    assert package["unresolved_responsibility"]["residual_owner"] == "operator"
    assert "legal_or_regulatory_compliance" in package["not_proven"]

    evaluation_types = {event["event_type"] for event in package["evidence"]["evaluation"]}
    execution_types = {event["event_type"] for event in package["evidence"]["execution_and_receipt"]}
    assert evaluation_types == {"external_evaluation_evidence_recorded"}
    assert "adapter_result" in execution_types
    assert evaluation_types.isdisjoint(execution_types)


def test_cli_audit_is_read_only_and_emits_json(tmp_path: Path, capsys) -> None:
    database = tmp_path / "rpos.db"
    service = _service_with_unresolved_operation(database)
    before = service.inspect("audit-001").state
    before_event_count = len(service.event_history("audit-001"))

    assert run(["--db", str(database), "audit", "audit-001"]) == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert payload["current_state"] == "effect_unknown"
    assert payload["unresolved_responsibility"]["required_authority"] == "operator"

    after = RposService(str(database))
    assert after.inspect("audit-001").state is before
    assert len(after.event_history("audit-001")) == before_event_count
