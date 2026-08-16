# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json

from rpos import (
    AdapterResult,
    OperationDefinition,
    ReceiptStatus,
    ReconciliationResult,
    ReconciliationStatus,
    RposService,
)


class UnknownEffectAdapter:
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return AdapterResult(
            receipt_status=ReceiptStatus.SUCCEEDED,
            receipt={"accepted": True},
            readback_verified=None,
            reason="receipt_without_effect_evidence",
        )


class UnavailableObserver:
    def observe(self, *, operation_id: str, latest_attempt: dict | None) -> ReconciliationResult:
        return ReconciliationResult(
            status=ReconciliationStatus.UNRESOLVED,
            evidence={"observer_available": False},
            reason="independent_observer_unavailable",
        )


def main() -> int:
    service = RposService()
    service.propose(
        OperationDefinition(
            operation_id="reconcile-unresolved-001",
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
    service.dispatch(
        "reconcile-unresolved-001",
        attempt_id="attempt-1",
        idempotency_key="external-effect-001",
        adapter=UnknownEffectAdapter(),
    )
    result = service.reconcile(
        "reconcile-unresolved-001",
        actor="operator",
        observer=UnavailableObserver(),
    )
    payload = {
        "state": result.state.value,
        "residual_owner": result.human_return.residual_owner if result.human_return else None,
        "required_authority": result.human_return.required_authority if result.human_return else None,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload == {
        "state": "effect_unknown",
        "residual_owner": "operator",
        "required_authority": "operator",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main())
