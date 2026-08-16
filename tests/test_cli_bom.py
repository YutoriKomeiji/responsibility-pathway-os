# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import json
from pathlib import Path

from rpos.cli import run
from rpos.models import OperationDefinition


def _definition() -> OperationDefinition:
    return OperationDefinition(
        operation_id="bom-proposal",
        action_name="write_resource",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="approver",
        human_return_point="review",
        residual_owner="operator",
        resume_authority="approver",
        requires_human_gate=True,
        verification_required=True,
    )


def test_propose_json_accepts_utf8_bom(tmp_path: Path, capsys) -> None:
    proposal = tmp_path / "proposal.json"
    proposal.write_text(json.dumps(_definition().to_dict()), encoding="utf-8-sig")

    assert run(["--db", str(tmp_path / "rpos.db"), "propose-json", str(proposal)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["state"] == "human_gate"
    assert payload["definition"]["operation_id"] == "bom-proposal"


def test_bom_input_still_fails_closed_for_non_object_json(tmp_path: Path, capsys) -> None:
    proposal = tmp_path / "proposal.json"
    proposal.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8-sig")

    assert run(["--db", str(tmp_path / "rpos.db"), "propose-json", str(proposal)]) == 2
    error = json.loads(capsys.readouterr().err)
    assert error["error"] == "ValueError"
    assert "must contain an object" in error["message"]
