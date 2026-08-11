# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path

from rpos import AdapterResult, OperationDefinition, OperationState, ReceiptStatus, RposService
from rpos.adapters import JsonlFileOperationAdapter, JsonlFileReconciliationObserver


class FailingAdapter:
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return AdapterResult(
            receipt_status=ReceiptStatus.FAILED,
            receipt={"accepted": False},
            readback_verified=False,
            readback=None,
            reason="demo_pre_dispatch_failure",
        )


def _definition(operation_id: str) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name="append_external_record",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="master",
        human_return_point="master-review",
        residual_owner="operator",
        resume_authority="master",
        requires_human_gate=True,
        verification_required=True,
    )


def test_jsonl_adapter_requires_separate_readback(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    sink = tmp_path / "external" / "effects.jsonl"
    operation_id = "op-file-readback"

    service.propose(_definition(operation_id))
    service.approve(operation_id, actor="master")
    result = service.dispatch(
        operation_id,
        attempt_id="attempt-1",
        idempotency_key="key-1",
        adapter=JsonlFileOperationAdapter(sink, {"value": 42}),
    )

    assert result.state is OperationState.EFFECT_UNKNOWN
    assert result.human_return is not None
    assert result.human_return.required_authority == "operator"

    reconciled = service.reconcile(
        operation_id,
        actor="operator",
        observer=JsonlFileReconciliationObserver(sink),
    )
    assert reconciled.state is OperationState.COMPLETED
    assert reconciled.human_return is None


def test_file_adapter_is_idempotent_for_same_operation_and_key(tmp_path: Path) -> None:
    sink = tmp_path / "effects.jsonl"
    adapter = JsonlFileOperationAdapter(sink, {"value": "once"})

    first = adapter.execute(operation_id="op-idempotent", attempt_id="a1", idempotency_key="key-1")
    second = adapter.execute(operation_id="op-idempotent", attempt_id="a2", idempotency_key="key-1")

    assert first.receipt["duplicate_prevented"] is False
    assert second.receipt["duplicate_prevented"] is True
    assert len(sink.read_text(encoding="utf-8").splitlines()) == 1


def test_repair_resume_then_external_readback_survives_restart(tmp_path: Path) -> None:
    database = tmp_path / "rpos.db"
    sink = tmp_path / "effects.jsonl"
    operation_id = "op-repair-resume"

    service = RposService(str(database))
    service.propose(_definition(operation_id))
    service.approve(operation_id, actor="master")

    failed = service.dispatch(
        operation_id,
        attempt_id="attempt-failed",
        idempotency_key="key-failed",
        adapter=FailingAdapter(),
    )
    assert failed.state is OperationState.REPAIR_REQUIRED

    ready = service.prepare_repair(operation_id, actor="operator", summary="replace failed demo adapter")
    assert ready.state is OperationState.READY_TO_RESUME

    authorized = service.resume(operation_id, actor="master")
    assert authorized.state is OperationState.AUTHORIZED

    unknown = service.dispatch(
        operation_id,
        attempt_id="attempt-file",
        idempotency_key="key-file",
        adapter=JsonlFileOperationAdapter(sink, {"message": "hello"}),
    )
    assert unknown.state is OperationState.EFFECT_UNKNOWN

    restarted = RposService(str(database))
    assert restarted.inspect(operation_id).state is OperationState.EFFECT_UNKNOWN

    completed = restarted.reconcile(
        operation_id,
        actor="operator",
        observer=JsonlFileReconciliationObserver(sink),
    )
    assert completed.state is OperationState.COMPLETED

    events = restarted.event_history(operation_id)
    assert events
    assert events[-1]["event_type"] == "state_transition"
    assert events[-1]["payload"]["to"] == "completed"
