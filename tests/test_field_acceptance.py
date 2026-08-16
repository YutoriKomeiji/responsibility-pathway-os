# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

from pathlib import Path

import pytest

from rpos import AdapterResult, OperationDefinition, ReceiptStatus, RposService


class CountingUnknownAdapter:
    def __init__(self) -> None:
        self.calls = 0

    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        self.calls += 1
        return AdapterResult(
            receipt_status=ReceiptStatus.SUCCEEDED,
            receipt={"accepted": True},
            readback_verified=None,
            reason="transport_succeeded_effect_not_verified",
        )


class FailingAdapter:
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return AdapterResult(
            receipt_status=ReceiptStatus.FAILED,
            receipt={"accepted": False},
            readback_verified=False,
            reason="deterministic_failure",
        )


def _definition(operation_id: str = "field-001") -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name="bounded_external_write",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="approver",
        human_return_point="operations-review",
        residual_owner="operator",
        resume_authority="approver",
        requires_human_gate=True,
        verification_required=True,
    )


def test_duplicate_idempotency_key_does_not_redispatch(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(_definition())
    service.approve("field-001", actor="approver")
    adapter = CountingUnknownAdapter()

    first = service.dispatch(
        "field-001",
        attempt_id="attempt-1",
        idempotency_key="stable-effect-key",
        adapter=adapter,
    )
    second = service.dispatch(
        "field-001",
        attempt_id="attempt-2",
        idempotency_key="stable-effect-key",
        adapter=adapter,
    )

    assert first.state.value == "effect_unknown"
    assert second.state.value == "effect_unknown"
    assert adapter.calls == 1


def test_human_return_authority_tracks_recovery_stage(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    proposed = service.propose(_definition())
    assert proposed.human_return is not None
    assert proposed.human_return.required_authority == "approver"
    assert proposed.human_return.unresolved_reason == "human_gate_decision_required"

    service.approve("field-001", actor="approver")
    failed = service.dispatch(
        "field-001",
        attempt_id="attempt-1",
        idempotency_key="failed-effect-key",
        adapter=FailingAdapter(),
    )
    assert failed.human_return is not None
    assert failed.human_return.required_authority == "operator"
    assert failed.human_return.unresolved_reason == "repair_required"

    ready = service.prepare_repair("field-001", actor="operator", summary="operator repaired integration")
    assert ready.human_return is not None
    assert ready.human_return.required_authority == "approver"
    assert ready.human_return.unresolved_reason == "resume_authorization_required"

    with pytest.raises(PermissionError):
        service.resume("field-001", actor="operator")
    resumed = service.resume("field-001", actor="approver")
    assert resumed.state.value == "authorized"
    assert resumed.human_return is None


def test_restart_preserves_effect_unknown_without_automatic_redispatch(tmp_path: Path) -> None:
    database = tmp_path / "rpos.db"
    service = RposService(str(database))
    service.propose(_definition())
    service.approve("field-001", actor="approver")
    adapter = CountingUnknownAdapter()
    service.dispatch(
        "field-001",
        attempt_id="attempt-1",
        idempotency_key="uncertain-effect-key",
        adapter=adapter,
    )
    assert adapter.calls == 1

    restarted = RposService(str(database))
    inspection = restarted.inspect("field-001")
    assert inspection.state.value == "effect_unknown"
    assert inspection.human_return is not None
    assert inspection.human_return.required_authority == "operator"
    assert adapter.calls == 1
