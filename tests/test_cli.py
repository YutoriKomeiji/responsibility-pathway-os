# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
from pathlib import Path

from rpos.cli import run
from rpos.models import OperationDefinition, OperationState
from rpos.service import RposService


def definition(operation_id: str, *, gate: bool = True) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name="write_resource",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="master" if gate else None,
        human_return_point="master-review",
        residual_owner="master",
        resume_authority="master",
        requires_human_gate=gate,
        verification_required=True,
    )


def test_boot_emits_json_without_mutation(tmp_path: Path, capsys) -> None:
    db = tmp_path / "rpos.db"
    service = RposService(str(db))
    service.propose(definition("op-boot"))
    before = service.inspect("op-boot").state
    assert run(["--db", str(db), "boot"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["operation_count"] == 1
    assert RposService(str(db)).inspect("op-boot").state is before


def test_propose_json_enters_expected_state(tmp_path: Path, capsys) -> None:
    db = tmp_path / "rpos.db"
    proposal = tmp_path / "proposal.json"
    proposal.write_text(json.dumps(definition("op-json").to_dict()), encoding="utf-8")
    assert run(["--db", str(db), "propose-json", str(proposal)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["state"] == "human_gate"


def test_inspect_preserves_human_return(tmp_path: Path, capsys) -> None:
    db = tmp_path / "rpos.db"
    RposService(str(db)).propose(definition("op-inspect"))
    assert run(["--db", str(db), "inspect", "op-inspect"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["human_return"]["required_authority"] == "master"


def test_events_exposes_ordered_durable_history_without_mutation(tmp_path: Path, capsys) -> None:
    db = tmp_path / "rpos.db"
    service = RposService(str(db))
    service.propose(definition("op-events"))
    before = service.inspect("op-events").state

    assert run(["--db", str(db), "events", "op-events"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["operation_id"] == "op-events"
    assert [event["event_type"] for event in payload["events"]] == ["operation_proposed", "state_transition"]
    assert payload["events"][0]["actor"] == "requester"
    assert payload["events"][1]["payload"]["to"] == "human_gate"
    assert RposService(str(db)).inspect("op-events").state is before


def test_wrong_approval_actor_is_nonzero_and_state_preserving(tmp_path: Path, capsys) -> None:
    db = tmp_path / "rpos.db"
    RposService(str(db)).propose(definition("op-denied"))
    assert run(["--db", str(db), "approve", "op-denied", "--actor", "wrong"]) == 2
    err = json.loads(capsys.readouterr().err)
    assert err["error"] == "PermissionError"
    assert RposService(str(db)).inspect("op-denied").state is OperationState.HUMAN_GATE


def test_unresolved_read_does_not_recover_dispatching_state(tmp_path: Path, capsys) -> None:
    db = tmp_path / "rpos.db"
    service = RposService(str(db))
    service.propose(definition("op-dispatching", gate=False))
    service.store.begin_attempt("op-dispatching", "a1", "k1")
    service._transition("op-dispatching", OperationState.DISPATCHING, actor="executor", reason="simulated")
    assert run(["--db", str(db), "unresolved"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert "op-dispatching" in payload["operation_ids"]
    assert RposService(str(db)).inspect("op-dispatching").state is OperationState.DISPATCHING
