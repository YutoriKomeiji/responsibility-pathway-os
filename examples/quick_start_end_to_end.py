# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from rpos import AdapterResult, OperationDefinition, ReceiptStatus, RposService
from rpos.adapters import JsonlFileOperationAdapter, JsonlFileReconciliationObserver


class DemoFailingAdapter:
    """Deterministic first-attempt failure used only to demonstrate repair/resume."""

    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return AdapterResult(
            receipt_status=ReceiptStatus.FAILED,
            receipt={"accepted": False},
            readback_verified=False,
            reason="demo_first_attempt_failed",
        )


def run_demo(workdir: Path) -> dict[str, object]:
    database = workdir / "rpos.db"
    sink = workdir / "external-effects.jsonl"
    operation_id = "quick-start-001"

    service = RposService(str(database))
    boot_before = service.boot_report()

    service.propose(
        OperationDefinition(
            operation_id=operation_id,
            action_name="append_external_record",
            requested_by="requester",
            execution_actor="executor",
            approval_authority="human_authority",
            human_return_point="human-authority-review",
            residual_owner="operator",
            resume_authority="human_authority",
            requires_human_gate=True,
            verification_required=True,
        )
    )
    service.approve(operation_id, actor="human_authority")

    first_attempt = service.dispatch(
        operation_id,
        attempt_id="attempt-1",
        idempotency_key="quick-start-failed-1",
        adapter=DemoFailingAdapter(),
    )
    service.prepare_repair(operation_id, actor="operator", summary="replace deterministic demo failure adapter")
    service.resume(operation_id, actor="human_authority")

    second_attempt = service.dispatch(
        operation_id,
        attempt_id="attempt-2",
        idempotency_key="quick-start-file-2",
        adapter=JsonlFileOperationAdapter(sink, {"message": "hello from RPOS"}),
    )

    restarted = RposService(str(database))
    after_restart = restarted.inspect(operation_id)
    final = restarted.reconcile(
        operation_id,
        actor="operator",
        observer=JsonlFileReconciliationObserver(sink),
    )

    return {
        "boot_before": {
            "operation_count": boot_before.operation_count,
            "unresolved_operation_ids": list(boot_before.unresolved_operation_ids),
        },
        "first_attempt_state": first_attempt.state.value,
        "second_attempt_state": second_attempt.state.value,
        "state_after_restart": after_restart.state.value,
        "final_state": final.state.value,
        "external_sink": str(sink),
        "event_history": restarted.event_history(operation_id),
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="rpos-quick-start-") as temp_dir:
        result = run_demo(Path(temp_dir))
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        if result["first_attempt_state"] != "repair_required":
            return 1
        if result["second_attempt_state"] != "effect_unknown":
            return 1
        if result["state_after_restart"] != "effect_unknown":
            return 1
        return 0 if result["final_state"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
