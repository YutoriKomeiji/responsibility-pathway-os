# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json

from rpos import AdapterResult, OperationDefinition, ReceiptStatus, RposService


class CountingAdapter:
    def __init__(self) -> None:
        self.calls = 0

    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        self.calls += 1
        return AdapterResult(
            receipt_status=ReceiptStatus.SUCCEEDED,
            receipt={"accepted": True},
            readback_verified=None,
            reason="effect_requires_independent_verification",
        )


def main() -> int:
    service = RposService()
    service.propose(
        OperationDefinition(
            operation_id="replay-guard-001",
            action_name="bounded_write",
            requested_by="requester",
            execution_actor="executor",
            approval_authority=None,
            human_return_point="operator-review",
            residual_owner="operator",
            requires_human_gate=False,
            verification_required=True,
        )
    )
    adapter = CountingAdapter()
    first = service.dispatch(
        "replay-guard-001",
        attempt_id="attempt-1",
        idempotency_key="semantic-effect-001",
        adapter=adapter,
    )
    second = service.dispatch(
        "replay-guard-001",
        attempt_id="attempt-2",
        idempotency_key="semantic-effect-001",
        adapter=adapter,
    )
    result = {
        "first_state": first.state.value,
        "second_state": second.state.value,
        "adapter_calls": adapter.calls,
        "human_return_required_authority": second.human_return.required_authority if second.human_return else None,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result == {
        "first_state": "effect_unknown",
        "second_state": "effect_unknown",
        "adapter_calls": 1,
        "human_return_required_authority": "operator",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main())
