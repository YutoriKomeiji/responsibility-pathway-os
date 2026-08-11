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


def definition(operation_id: str) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name="write_resource",
        requested_by="requester",
        execution_actor="executor",
        approval_authority=None,
        human_return_point="master-review",
        residual_owner="repair-owner",
        resume_authority="resume-owner",
        requires_human_gate=False,
        verification_required=True,
    )


def failed_operation(service: RposService, operation_id: str) -> CountingAdapter:
    service.propose(definition(operation_id))
    adapter = CountingAdapter(AdapterResult(ReceiptStatus.FAILED, {}, False, {}, "write_failed"))
    result = service.dispatch(operation_id, attempt_id="a1", idempotency_key="k1", adapter=adapter)
    assert result.state is OperationState.REPAIR_REQUIRED
    return adapter


def test_only_residual_owner_may_prepare_repair(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    failed_operation(service, "op-owner")
    with pytest.raises(PermissionError):
        service.prepare_repair("op-owner", actor="someone-else", summary="fixed precondition")
    assert service.inspect("op-owner").state is OperationState.REPAIR_REQUIRED


def test_repair_preparation_enters_ready_to_resume_and_retains_human_return(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    failed_operation(service, "op-ready")
    result = service.prepare_repair("op-ready", actor="repair-owner", summary="fixed precondition")
    assert result.state is OperationState.READY_TO_RESUME
    assert result.human_return is not None
    assert result.human_return.required_authority == "resume-owner"
    assert result.human_return.unresolved_reason == "resume_authorization_required"


def test_only_resume_authority_may_resume(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    failed_operation(service, "op-resume-auth")
    service.prepare_repair("op-resume-auth", actor="repair-owner", summary="fixed")
    with pytest.raises(PermissionError):
        service.resume("op-resume-auth", actor="repair-owner")
    assert service.inspect("op-resume-auth").state is OperationState.READY_TO_RESUME


def test_resume_authorizes_without_adapter_invocation(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    adapter = failed_operation(service, "op-resume")
    assert adapter.calls == 1
    service.prepare_repair("op-resume", actor="repair-owner", summary="fixed")
    result = service.resume("op-resume", actor="resume-owner")
    assert result.state is OperationState.AUTHORIZED
    assert adapter.calls == 1


def test_fresh_dispatch_after_resume_can_complete(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    failed_operation(service, "op-redo")
    service.prepare_repair("op-redo", actor="repair-owner", summary="fixed")
    service.resume("op-redo", actor="resume-owner")
    adapter = CountingAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {"accepted": True}, True, {"exists": True}))
    result = service.dispatch("op-redo", attempt_id="a2", idempotency_key="k2", adapter=adapter)
    assert result.state is OperationState.COMPLETED
    assert adapter.calls == 1


def test_restart_preserves_ready_to_resume_without_dispatch(tmp_path: Path) -> None:
    database = tmp_path / "rpos.db"
    first = RposService(str(database))
    adapter = failed_operation(first, "op-restart-ready")
    first.prepare_repair("op-restart-ready", actor="repair-owner", summary="fixed")
    assert adapter.calls == 1

    restarted = RposService(str(database))
    assert restarted.inspect("op-restart-ready").state is OperationState.READY_TO_RESUME
    assert "op-restart-ready" in restarted.boot_report().unresolved_operation_ids
    assert restarted.recover_incomplete_dispatches() == ()
    assert adapter.calls == 1


def test_old_idempotency_key_is_not_reused_by_resume(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    adapter = failed_operation(service, "op-idem")
    service.prepare_repair("op-idem", actor="repair-owner", summary="fixed")
    service.resume("op-idem", actor="resume-owner")

    replay_adapter = CountingAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {}, True, {}))
    result = service.dispatch("op-idem", attempt_id="a2", idempotency_key="k1", adapter=replay_adapter)
    assert result.state is OperationState.AUTHORIZED
    assert replay_adapter.calls == 0
    assert adapter.calls == 1
