# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import json

from rpos import AdapterResult, OperationDefinition, ReceiptStatus, RposService


class VerifiedDemoAdapter:
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return AdapterResult(
            receipt_status=ReceiptStatus.SUCCEEDED,
            receipt={"accepted": True, "attempt_id": attempt_id},
            readback_verified=True,
            readback={"operation_id": operation_id, "applied": True},
            reason="bounded_demo_readback_verified",
        )


def main() -> int:
    service = RposService()
    operation_id = "example-happy-001"
    service.propose(OperationDefinition(
        operation_id=operation_id,
        action_name="bounded_demo_action",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="human_authority",
        human_return_point="human-authority-review",
        residual_owner="operator",
        resume_authority="human_authority",
        requires_human_gate=True,
        verification_required=True,
    ))
    service.approve(operation_id, actor="human_authority")
    final = service.dispatch(
        operation_id,
        attempt_id="attempt-1",
        idempotency_key="happy-1",
        adapter=VerifiedDemoAdapter(),
    )
    print(json.dumps({"state": final.state.value, "events": service.event_history(operation_id)}, indent=2))
    return 0 if final.state.value == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
