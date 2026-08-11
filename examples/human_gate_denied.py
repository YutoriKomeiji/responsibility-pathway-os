# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import json

from rpos import OperationDefinition, RposService


def main() -> int:
    service = RposService()
    operation_id = "example-denied-001"
    pending = service.propose(OperationDefinition(
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
    denied = service.deny(operation_id, actor="human_authority", reason="example_policy_decision")
    print(json.dumps({
        "before": pending.state.value,
        "after": denied.state.value,
        "events": service.event_history(operation_id),
    }, indent=2))
    return 0 if pending.state.value == "human_gate" and denied.state.value == "denied" else 1


if __name__ == "__main__":
    raise SystemExit(main())
