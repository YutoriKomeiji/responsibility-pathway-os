# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json

from rpos import OperationDefinition, RposService


class RaisingAdapter:
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str):
        raise RuntimeError("simulated adapter transport failure")


def main() -> int:
    service = RposService()
    service.propose(
        OperationDefinition(
            operation_id="adapter-exception-001",
            action_name="bounded_external_write",
            requested_by="requester",
            execution_actor="executor",
            approval_authority=None,
            human_return_point="operator-review",
            residual_owner="operator",
            requires_human_gate=False,
            verification_required=True,
        )
    )
    result = service.dispatch(
        "adapter-exception-001",
        attempt_id="attempt-1",
        idempotency_key="external-effect-001",
        adapter=RaisingAdapter(),
    )
    payload = {
        "state": result.state.value,
        "required_authority": result.human_return.required_authority if result.human_return else None,
        "unresolved_reason": result.human_return.unresolved_reason if result.human_return else None,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["state"] == "effect_unknown" and payload["required_authority"] == "operator" else 1


if __name__ == "__main__":
    raise SystemExit(main())
