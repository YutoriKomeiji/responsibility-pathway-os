# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from rpos import OperationDefinition, RposService
from rpos.adapters import JsonlFileOperationAdapter, JsonlFileReconciliationObserver


def run(workdir: Path) -> dict[str, object]:
    database = workdir / "rpos.db"
    sink = workdir / "effects.jsonl"
    operation_id = "example-unknown-restart-001"

    service = RposService(str(database))
    service.propose(OperationDefinition(
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
    ))
    service.approve(operation_id, actor="human_authority")
    after_receipt = service.dispatch(
        operation_id,
        attempt_id="attempt-1",
        idempotency_key="unknown-restart-1",
        adapter=JsonlFileOperationAdapter(sink, {"message": "external effect"}),
    )

    restarted = RposService(str(database))
    after_restart = restarted.inspect(operation_id)
    final = restarted.reconcile(
        operation_id,
        actor="operator",
        observer=JsonlFileReconciliationObserver(sink),
    )
    return {
        "after_receipt": after_receipt.state.value,
        "after_restart": after_restart.state.value,
        "final": final.state.value,
        "events": restarted.event_history(operation_id),
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="rpos-unknown-") as temp:
        result = run(Path(temp))
        print(json.dumps(result, indent=2))
        expected = ("effect_unknown", "effect_unknown", "completed")
        actual = (result["after_receipt"], result["after_restart"], result["final"])
        return 0 if actual == expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
