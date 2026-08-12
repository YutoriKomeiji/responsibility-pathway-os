# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

from rpos import (
    AdapterResult,
    OperationDefinition,
    OperationState,
    ReceiptStatus,
    ReconciliationResult,
    ReconciliationStatus,
    RposService,
)
from rpos.observatory import ResponsibilityObservatory


class _ReceiptOnlyAdapter:
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return AdapterResult(
            receipt_status=ReceiptStatus.SUCCEEDED,
            receipt={"accepted": True},
            readback_verified=None,
            reason="receipt_without_independent_effect_verification",
        )


class _VerifiedAdapter:
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return AdapterResult(
            receipt_status=ReceiptStatus.SUCCEEDED,
            receipt={"accepted": True},
            readback_verified=True,
            readback={"operation_id": operation_id, "applied": True},
            reason="independent_readback_verified",
        )


class _NotAppliedObserver:
    def observe(self, *, operation_id: str, latest_attempt: dict[str, object] | None) -> ReconciliationResult:
        return ReconciliationResult(
            status=ReconciliationStatus.VERIFIED_NOT_APPLIED,
            evidence={"operation_id": operation_id, "observed": "not_applied"},
            reason="authoritative_readback_not_applied",
        )


def _definition(operation_id: str, *, human_gate: bool = False, resume_authority: str | None = None) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name="bounded_demo_action",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="approver" if human_gate else None,
        human_return_point="return-to-console",
        residual_owner="operator",
        resume_authority=resume_authority,
        requires_human_gate=human_gate,
        verification_required=True,
    )


def _assert_observation_did_not_mutate(service: RposService, operation_id: str, before_state: OperationState, before_events: list[dict[str, object]]) -> None:
    after = service.inspect(operation_id)
    after_events = service.event_history(operation_id)
    assert after.state is before_state
    assert after_events == before_events


def test_observe_human_gate_is_read_only_and_identifies_authority() -> None:
    service = RposService()
    service.propose(_definition("op-human-gate", human_gate=True))
    observatory = ResponsibilityObservatory(service)
    before = service.inspect("op-human-gate")
    before_events = service.event_history("op-human-gate")

    observation = observatory.observe("op-human-gate")

    assert observation.state is OperationState.HUMAN_GATE
    assert observation.required_authority == "approver"
    assert observation.residual_owner == "operator"
    assert observation.human_return_point == "return-to-console"
    assert observation.unresolved_reason == "human_gate_decision_required"
    assert observation.allowed_next_actions == ("human_gate_decision",)
    assert observation.event_count == len(before_events)
    _assert_observation_did_not_mutate(service, "op-human-gate", before.state, before_events)


def test_observe_effect_unknown_preserves_uncertainty_and_is_read_only() -> None:
    service = RposService()
    service.propose(_definition("op-effect-unknown"))
    service.dispatch(
        "op-effect-unknown",
        attempt_id="attempt-1",
        idempotency_key="key-1",
        adapter=_ReceiptOnlyAdapter(),
    )
    observatory = ResponsibilityObservatory(service)
    before = service.inspect("op-effect-unknown")
    before_events = service.event_history("op-effect-unknown")

    observation = observatory.observe("op-effect-unknown")

    assert observation.state is OperationState.EFFECT_UNKNOWN
    assert observation.required_authority == "operator"
    assert observation.unresolved_reason == "external_effect_not_verified"
    assert observation.allowed_next_actions == ("reconcile",)
    _assert_observation_did_not_mutate(service, "op-effect-unknown", before.state, before_events)


def test_observe_ready_to_resume_does_not_authorize_resume() -> None:
    service = RposService()
    service.propose(_definition("op-resume", resume_authority="resume-approver"))
    service.dispatch(
        "op-resume",
        attempt_id="attempt-1",
        idempotency_key="key-1",
        adapter=_ReceiptOnlyAdapter(),
    )
    service.reconcile("op-resume", actor="operator", observer=_NotAppliedObserver())
    service.prepare_repair("op-resume", actor="operator", summary="prepared bounded repair")
    observatory = ResponsibilityObservatory(service)
    before_events = service.event_history("op-resume")

    observation = observatory.observe("op-resume")

    assert observation.state is OperationState.READY_TO_RESUME
    assert observation.required_authority == "resume-approver"
    assert observation.unresolved_reason == "resume_authorization_required"
    assert observation.allowed_next_actions == ("request_resume_authorization",)
    assert service.inspect("op-resume").state is OperationState.READY_TO_RESUME
    assert service.event_history("op-resume") == before_events


def test_observe_completed_exposes_no_next_mutation_guidance() -> None:
    service = RposService()
    service.propose(_definition("op-completed"))
    service.dispatch(
        "op-completed",
        attempt_id="attempt-1",
        idempotency_key="key-1",
        adapter=_VerifiedAdapter(),
    )
    observatory = ResponsibilityObservatory(service)
    before_events = service.event_history("op-completed")

    observation = observatory.observe("op-completed")

    assert observation.state is OperationState.COMPLETED
    assert observation.required_authority is None
    assert observation.unresolved_reason is None
    assert observation.allowed_next_actions == ()
    assert service.event_history("op-completed") == before_events


def test_repeated_observation_is_stable_for_unchanged_state() -> None:
    service = RposService()
    service.propose(_definition("op-stable", human_gate=True))
    observatory = ResponsibilityObservatory(service)
    before_events = service.event_history("op-stable")

    first = observatory.observe("op-stable")
    second = observatory.observe("op-stable")

    assert first == second
    assert service.event_history("op-stable") == before_events
