# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path

import pytest

from rpos import AdapterResult, OperationDefinition, OperationState, ReceiptStatus, RposService


class CountingAdapter:
    def __init__(self, result: AdapterResult) -> None:
        self.result = result
        self.calls = 0

    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        self.calls += 1
        return self.result


def definition(operation_id: str, *, gate: bool = True) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name="write_resource",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="master" if gate else None,
        human_return_point="master-review",
        residual_owner="master",
        requires_human_gate=gate,
        verification_required=True,
    )


def test_gated_operation_cannot_dispatch_before_approval(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(definition("op-gate"))
    adapter = CountingAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {}, True, {}))
    with pytest.raises(PermissionError):
        service.dispatch("op-gate", attempt_id="a1", idempotency_key="k1", adapter=adapter)
    assert adapter.calls == 0
    assert service.inspect("op-gate").latest_attempt is None


def test_wrong_approval_authority_is_rejected(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(definition("op-auth"))
    with pytest.raises(PermissionError):
        service.approve("op-auth", actor="someone-else")
    assert service.inspect("op-auth").state is OperationState.HUMAN_GATE


def test_success_receipt_without_readback_is_effect_unknown(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(definition("op-unknown", gate=False))
    adapter = CountingAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {"accepted": True}, None, None))
    result = service.dispatch("op-unknown", attempt_id="a1", idempotency_key="k1", adapter=adapter)
    assert result.state is OperationState.EFFECT_UNKNOWN
    assert result.human_return is not None
    assert result.human_return.residual_owner == "master"


def test_verified_readback_completes(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(definition("op-complete", gate=False))
    adapter = CountingAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {"accepted": True}, True, {"exists": True}))
    result = service.dispatch("op-complete", attempt_id="a1", idempotency_key="k1", adapter=adapter)
    assert result.state is OperationState.COMPLETED
    assert result.human_return is None


def test_adapter_failure_requires_repair(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(definition("op-fail", gate=False))
    adapter = CountingAdapter(AdapterResult(ReceiptStatus.FAILED, {}, False, {}, "write_failed"))
    result = service.dispatch("op-fail", attempt_id="a1", idempotency_key="k1", adapter=adapter)
    assert result.state is OperationState.REPAIR_REQUIRED
    assert result.human_return is not None


def test_idempotency_key_does_not_redispatch_after_success(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(definition("op-replay", gate=False))
    adapter = CountingAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {}, True, {}))
    first = service.dispatch("op-replay", attempt_id="a1", idempotency_key="same", adapter=adapter)
    second = service.dispatch("op-replay", attempt_id="a2", idempotency_key="same", adapter=adapter)
    assert first.state is OperationState.COMPLETED
    assert second.state is OperationState.COMPLETED
    assert adapter.calls == 1


def test_restart_recovery_does_not_redispatch(tmp_path: Path) -> None:
    database = tmp_path / "rpos.db"
    first = RposService(str(database))
    first.propose(definition("op-restart", gate=False))
    first.store.begin_attempt("op-restart", "a1", "k1")
    first._transition("op-restart", OperationState.DISPATCHING, actor="executor", reason="simulated_crash_after_dispatch_start")

    restarted = RposService(str(database))
    before = restarted.boot_report()
    assert "op-restart" in before.unresolved_operation_ids
    recovered = restarted.recover_incomplete_dispatches()
    assert recovered == ("op-restart",)
    assert restarted.inspect("op-restart").state is OperationState.EFFECT_UNKNOWN


def test_dispatch_start_transaction_rolls_back_before_external_effect(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    database = tmp_path / "rpos.db"
    service = RposService(str(database))
    service.propose(definition("op-start-crash", gate=False))
    adapter = CountingAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {}, True, {}))
    original_record_event = service.store.record_event

    def crash_after_dispatch_transition(operation_id: str, event_type: str, actor: str, payload: dict[str, object]) -> None:
        original_record_event(operation_id, event_type, actor, payload)
        if event_type == "state_transition" and payload.get("to") == OperationState.DISPATCHING.value:
            raise RuntimeError("simulated crash before dispatch-start commit")

    monkeypatch.setattr(service.store, "record_event", crash_after_dispatch_transition)
    with pytest.raises(RuntimeError, match="dispatch-start"):
        service.dispatch("op-start-crash", attempt_id="a1", idempotency_key="k1", adapter=adapter)

    assert adapter.calls == 0
    restarted = RposService(str(database))
    inspection = restarted.inspect("op-start-crash")
    assert inspection.state is OperationState.AUTHORIZED
    assert inspection.latest_attempt is None
    assert all(
        not (event["event_type"] == "state_transition" and event["payload"].get("to") == "dispatching")
        for event in restarted.event_history("op-start-crash")
    )


def test_dispatch_result_transaction_rolls_back_to_recoverable_dispatching(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "rpos.db"
    service = RposService(str(database))
    service.propose(definition("op-result-crash", gate=False))
    adapter = CountingAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {"accepted": True}, True, {"exists": True}))
    original_record_event = service.store.record_event

    def crash_after_adapter_result(operation_id: str, event_type: str, actor: str, payload: dict[str, object]) -> None:
        original_record_event(operation_id, event_type, actor, payload)
        if event_type == "adapter_result":
            raise RuntimeError("simulated crash before result commit")

    monkeypatch.setattr(service.store, "record_event", crash_after_adapter_result)
    with pytest.raises(RuntimeError, match="result commit"):
        service.dispatch("op-result-crash", attempt_id="a1", idempotency_key="k1", adapter=adapter)

    assert adapter.calls == 1
    restarted = RposService(str(database))
    stranded = restarted.inspect("op-result-crash")
    assert stranded.state is OperationState.DISPATCHING
    assert stranded.latest_attempt is not None
    assert stranded.latest_attempt["dispatch_finished"] == 0
    assert all(event["event_type"] != "adapter_result" for event in restarted.event_history("op-result-crash"))

    recovered = restarted.recover_incomplete_dispatches()
    assert recovered == ("op-result-crash",)
    assert restarted.inspect("op-result-crash").state is OperationState.EFFECT_UNKNOWN


def test_restart_recovers_legacy_finished_attempt_stranded_in_dispatching(tmp_path: Path) -> None:
    database = tmp_path / "rpos.db"
    first = RposService(str(database))
    first.propose(definition("op-legacy-finished", gate=False))
    first.store.begin_attempt("op-legacy-finished", "a1", "k1")
    first._transition(
        "op-legacy-finished",
        OperationState.DISPATCHING,
        actor="executor",
        reason="simulate_pre_fix_dispatch_start",
    )
    first.store.finish_attempt(
        "a1",
        receipt_status=ReceiptStatus.SUCCEEDED.value,
        readback_verified=True,
        result_reason="simulate_pre_fix_crash_after_finish_attempt",
    )

    restarted = RposService(str(database))
    stranded = restarted.inspect("op-legacy-finished")
    assert stranded.state is OperationState.DISPATCHING
    assert stranded.latest_attempt is not None
    assert stranded.latest_attempt["dispatch_finished"] == 1

    recovered = restarted.recover_incomplete_dispatches()
    assert recovered == ("op-legacy-finished",)
    assert restarted.inspect("op-legacy-finished").state is OperationState.EFFECT_UNKNOWN


def test_state_transition_and_event_roll_back_together(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    database = tmp_path / "rpos.db"
    service = RposService(str(database))
    service.propose(definition("op-transition-crash"))
    original_record_event = service.store.record_event

    def crash_after_transition_event(operation_id: str, event_type: str, actor: str, payload: dict[str, object]) -> None:
        original_record_event(operation_id, event_type, actor, payload)
        if event_type == "state_transition" and payload.get("to") == OperationState.AUTHORIZED.value:
            raise RuntimeError("simulated crash before transition commit")

    monkeypatch.setattr(service.store, "record_event", crash_after_transition_event)
    with pytest.raises(RuntimeError, match="transition commit"):
        service.approve("op-transition-crash", actor="master")

    restarted = RposService(str(database))
    assert restarted.inspect("op-transition-crash").state is OperationState.HUMAN_GATE
    assert all(
        not (event["event_type"] == "state_transition" and event["payload"].get("to") == "authorized")
        for event in restarted.event_history("op-transition-crash")
    )


def test_unresolved_inspection_retains_human_return(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    inspection = service.propose(definition("op-return"))
    assert inspection.human_return is not None
    assert inspection.human_return.human_return_point == "master-review"
    assert inspection.human_return.residual_owner == "master"
    assert inspection.human_return.required_authority == "master"
