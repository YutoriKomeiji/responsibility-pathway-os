# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json

from rpos import AdapterResult, OperationDefinition, ReceiptStatus, RposService


class FailingAdapter:
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return AdapterResult(
            receipt_status=ReceiptStatus.FAILED,
            receipt={"accepted": False},
            readback_verified=False,
            reason="repair_required_demo",
        )


def main() -> int:
    service = RposService()
    proposed = service.propose(
        OperationDefinition(
            operation_id="human-return-001",
            action_name="bounded_write",
            requested_by="requester",
            execution_actor="executor",
            approval_authority="approver",
            human_return_point="change-review-board",
            residual_owner="operator",
            resume_authority="approver",
            requires_human_gate=True,
            verification_required=True,
        )
    )
    initial_authority = proposed.human_return.required_authority if proposed.human_return else None
    service.approve("human-return-001", actor="approver")
    failed = service.dispatch(
        "human-return-001",
        attempt_id="attempt-1",
        idempotency_key="failed-001",
        adapter=FailingAdapter(),
    )
    repair_authority = failed.human_return.required_authority if failed.human_return else None
    ready = service.prepare_repair("human-return-001", actor="operator", summary="bounded repair prepared")
    resume_authority = ready.human_return.required_authority if ready.human_return else None
    resumed = service.resume("human-return-001", actor="approver")

    result = {
        "initial_gate_authority": initial_authority,
        "repair_owner": repair_authority,
        "resume_authority": resume_authority,
        "state_after_explicit_resume": resumed.state.value,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result == {
        "initial_gate_authority": "approver",
        "repair_owner": "operator",
        "resume_authority": "approver",
        "state_after_explicit_resume": "authorized",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main())
