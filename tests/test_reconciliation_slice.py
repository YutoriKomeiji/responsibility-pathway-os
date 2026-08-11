# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path

import pytest

from rpos import (
    AdapterResult,
    OperationDefinition,
    OperationState,
    ReceiptStatus,
    ReconciliationResult,
    ReconciliationStatus,
    RposService,
)


class CountingAdapter:
    def __init__(self) -> None:
        self.calls = 0

    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        self.calls += 1
        return AdapterResult(
            ReceiptStatus.SUCCEEDED,
            {"accepted": True},
            None,
            None,
            "receipt_without_independent_readback",
        )


class Observer:
    def __init__(self, result: ReconciliationResult) -> None:
        self.result = result
        self.calls = 0

    def observe(self, *, operation_id: str, latest_attempt: dict | None) -> ReconciliationResult:
        self.calls += 1
        return self.result


class RaisingObserver:
    def observe(self, *, operation_id: str, latest_attempt: dict | None) -> ReconciliationResult:
        raise RuntimeError("observer unavailable")


def definition(operation_id: str) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name="write_resource",
        requested_by="requester",
        execution_actor="executor",
        approval_authority=None,
        human_return_point="master-review",
        residual_owner="master",
        requires_human_gate=False,
        verification_required=True,
    )


def unknown_operation(tmp_path: Path, operation_id: str) -> tuple[RposService, CountingAdapter]:
    service = RposService(str(tmp_path / f"{operation_id}.db"))
    service.propose(definition(operation_id))
    adapter = CountingAdapter()
    result = service.dispatch(operation_id, attempt_id="a1", idempotency_key="k1", adapter=adapter)
    assert result.state is OperationState.EFFECT_UNKNOWN
    return service, adapter


def test_wrong_actor_cannot_reconcile(tmp_path: Path) -> None:
    service, _ = unknown_operation(tmp_path, "op-wrong-actor")
    observer = Observer(ReconciliationResult(ReconciliationStatus.UNRESOLVED, {"checked": True}))
    with pytest.raises(PermissionError):
        service.reconcile("op-wrong-actor", actor="someone-else", observer=observer)
    assert observer.calls == 0


def test_verified_applied_completes_without_redispatch(tmp_path: Path) -> None:
    service, adapter = unknown_operation(tmp_path, "op-applied")
    observer = Observer(
        ReconciliationResult(
            ReconciliationStatus.VERIFIED_APPLIED,
            {"resource_exists": True},
            "independent_readback_found_effect",
        )
    )
    result = service.reconcile("op-applied", actor="master", observer=observer)
    assert result.state is OperationState.COMPLETED
    assert adapter.calls == 1
    assert observer.calls == 1


def test_verified_applied_requires_evidence(tmp_path: Path) -> None:
    service, _ = unknown_operation(tmp_path, "op-empty-evidence")
    observer = Observer(ReconciliationResult(ReconciliationStatus.VERIFIED_APPLIED, {}))
    with pytest.raises(ValueError):
        service.reconcile("op-empty-evidence", actor="master", observer=observer)
    assert service.inspect("op-empty-evidence").state is OperationState.EFFECT_UNKNOWN


def test_verified_not_applied_requires_repair(tmp_path: Path) -> None:
    service, adapter = unknown_operation(tmp_path, "op-not-applied")
    observer = Observer(
        ReconciliationResult(
            ReconciliationStatus.VERIFIED_NOT_APPLIED,
            {"resource_exists": False},
            "independent_readback_found_no_effect",
        )
    )
    result = service.reconcile("op-not-applied", actor="master", observer=observer)
    assert result.state is OperationState.REPAIR_REQUIRED
    assert result.human_return is not None
    assert adapter.calls == 1


def test_unresolved_reconciliation_preserves_unknown_and_human_return(tmp_path: Path) -> None:
    service, adapter = unknown_operation(tmp_path, "op-still-unknown")
    observer = Observer(
        ReconciliationResult(
            ReconciliationStatus.UNRESOLVED,
            {"endpoint_reachable": False},
            "independent_source_unavailable",
        )
    )
    result = service.reconcile("op-still-unknown", actor="master", observer=observer)
    assert result.state is OperationState.EFFECT_UNKNOWN
    assert result.human_return is not None
    assert result.human_return.residual_owner == "master"
    assert adapter.calls == 1


def test_reconciliation_exception_stays_unknown(tmp_path: Path) -> None:
    service, adapter = unknown_operation(tmp_path, "op-observer-error")
    result = service.reconcile("op-observer-error", actor="master", observer=RaisingObserver())
    assert result.state is OperationState.EFFECT_UNKNOWN
    assert result.human_return is not None
    assert adapter.calls == 1
