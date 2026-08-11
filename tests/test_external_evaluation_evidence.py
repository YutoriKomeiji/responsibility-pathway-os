# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path

import pytest

from rpos import (
    EvaluationEvidenceClass,
    ExternalEvaluationEvidence,
    OperationDefinition,
    OperationState,
    RposService,
)


def _gated_definition(operation_id: str) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
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


def test_external_evaluation_evidence_does_not_authorize_dispatch(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    proposed = service.propose(_gated_definition("eval-evidence-001"))
    assert proposed.state is OperationState.HUMAN_GATE

    evidence = ExternalEvaluationEvidence(
        evidence_id="safety-eval-001",
        evidence_class=EvaluationEvidenceClass.SAFETY_EVALUATION,
        source_system="external-safety-evaluator",
        source_reference="evaluation-run-001",
        evaluation_scope="bounded safety evaluation profile",
        result_summary="evaluation completed with recorded metrics",
        artifact_digest="sha256:example",
    )
    after_record = service.record_evaluation_evidence(
        "eval-evidence-001",
        actor="evidence_producer",
        evidence=evidence,
    )

    assert after_record.state is OperationState.HUMAN_GATE
    assert after_record.latest_attempt is None
    with pytest.raises(PermissionError):
        service.dispatch(
            "eval-evidence-001",
            attempt_id="attempt-1",
            idempotency_key="dispatch-1",
            adapter=object(),  # type: ignore[arg-type]
        )

    events = service.event_history("eval-evidence-001")
    recorded = [event for event in events if event["event_type"] == "external_evaluation_evidence_recorded"]
    assert len(recorded) == 1
    assert recorded[0]["payload"]["evidence"]["evidence_class"] == "safety_evaluation"


def test_external_evaluation_evidence_persists_without_state_promotion(tmp_path: Path) -> None:
    database = tmp_path / "rpos.db"
    service = RposService(str(database))
    service.propose(_gated_definition("eval-evidence-002"))
    service.record_evaluation_evidence(
        "eval-evidence-002",
        actor="evidence_producer",
        evidence=ExternalEvaluationEvidence(
            evidence_id="capability-eval-001",
            evidence_class=EvaluationEvidenceClass.CAPABILITY_EVALUATION,
            source_system="external-capability-evaluator",
            source_reference="evaluation-run-002",
            evaluation_scope="Japanese language capability evaluation",
            result_summary="evaluation outputs retained for responsible review",
        ),
    )

    restarted = RposService(str(database))
    inspection = restarted.inspect("eval-evidence-002")
    assert inspection.state is OperationState.HUMAN_GATE

    events = restarted.event_history("eval-evidence-002")
    assert any(event["event_type"] == "external_evaluation_evidence_recorded" for event in events)
    assert not any(
        event["event_type"] == "state_transition" and event["payload"].get("to") == "authorized"
        for event in events
    )
