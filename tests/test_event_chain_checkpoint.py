# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT

from rpos import OperationDefinition, RposService, build_event_chain_checkpoint, event_chain_matches


def _definition() -> OperationDefinition:
    return OperationDefinition(
        operation_id="op-chain-1",
        action_name="bounded-write",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="approver",
        human_return_point="review-desk",
        residual_owner="owner",
        requires_human_gate=True,
    )


def test_service_event_chain_checkpoint_is_stable_for_unchanged_history() -> None:
    service = RposService()
    service.propose(_definition())
    first = service.event_chain_checkpoint("op-chain-1")
    second = service.event_chain_checkpoint("op-chain-1")
    assert first == second
    assert first.event_count == 2


def test_appending_event_changes_checkpoint_without_invalidating_old_history() -> None:
    service = RposService()
    service.propose(_definition())
    before = service.event_chain_checkpoint("op-chain-1")
    service.approve("op-chain-1", actor="approver")
    after = service.event_chain_checkpoint("op-chain-1")
    assert after.event_count == before.event_count + 1
    assert after.chain_digest != before.chain_digest


def test_mutating_historical_event_breaks_retained_checkpoint() -> None:
    service = RposService()
    service.propose(_definition())
    retained = service.event_chain_checkpoint("op-chain-1")

    service.store.connection.execute(
        "UPDATE events SET actor = ? WHERE operation_id = ? AND seq = (SELECT MIN(seq) FROM events WHERE operation_id = ?)",
        ("attacker", "op-chain-1", "op-chain-1"),
    )
    service.store.connection.commit()

    assert service.event_chain_checkpoint("op-chain-1") != retained
    assert not event_chain_matches(retained, service.event_history("op-chain-1"))


def test_checkpoint_builder_rejects_cross_operation_event_substitution() -> None:
    service = RposService()
    service.propose(_definition())
    events = service.event_history("op-chain-1")
    tampered = [dict(events[0]), dict(events[1])]
    tampered[1]["operation_id"] = "op-other"

    try:
        build_event_chain_checkpoint("op-chain-1", tampered)
    except ValueError as exc:
        assert "operation_id" in str(exc)
    else:
        raise AssertionError("cross-operation event substitution must be rejected")


def test_checkpoint_builder_rejects_non_monotonic_sequence() -> None:
    service = RposService()
    service.propose(_definition())
    events = service.event_history("op-chain-1")
    reversed_events = list(reversed(events))

    try:
        build_event_chain_checkpoint("op-chain-1", reversed_events)
    except ValueError as exc:
        assert "strictly ordered" in str(exc)
    else:
        raise AssertionError("non-monotonic event sequence must be rejected")
