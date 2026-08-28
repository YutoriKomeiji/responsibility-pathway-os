# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from datetime import datetime, timedelta, timezone

from rpos.security import (
    AuthorityEnvelope,
    CommitAuthorityEnvelope,
    ResponsibilityIntegritySnapshot,
    SecurityDisposition,
    find_responsibility_inconsistencies,
    validate_authority_envelope,
    validate_commit_authority,
)


NOW = datetime(2026, 8, 12, 0, 0, tzinfo=timezone.utc)


def _envelope(**overrides: object) -> AuthorityEnvelope:
    values: dict[str, object] = {
        "actor": "approver-a",
        "operation_id": "op-1",
        "action_name": "bounded-write",
        "issued_at": NOW - timedelta(minutes=1),
        "expires_at": NOW + timedelta(minutes=5),
        "evidence_digest": "evidence-v1",
        "context_digest": "context-v1",
    }
    values.update(overrides)
    return AuthorityEnvelope(**values)  # type: ignore[arg-type]


def _validate(envelope: AuthorityEnvelope):
    return validate_authority_envelope(
        envelope,
        now=NOW,
        expected_actor="approver-a",
        expected_operation_id="op-1",
        expected_action_name="bounded-write",
        expected_evidence_digest="evidence-v1",
        expected_context_digest="context-v1",
    )


def _commit_envelope(**overrides: object) -> CommitAuthorityEnvelope:
    values: dict[str, object] = {
        "actor": "approver-a",
        "operation_id": "op-1",
        "action_name": "bounded-write",
        "target_digest": "target-v1",
        "effect_digest": "effect-v1",
        "issued_at": NOW - timedelta(minutes=1),
        "expires_at": NOW + timedelta(minutes=5),
        "evidence_digest": "evidence-v1",
        "context_digest": "context-v1",
        "authority_epoch": 7,
        "consumed": False,
    }
    values.update(overrides)
    return CommitAuthorityEnvelope(**values)  # type: ignore[arg-type]


def _validate_commit(envelope: CommitAuthorityEnvelope):
    return validate_commit_authority(
        envelope,
        now=NOW,
        expected_actor="approver-a",
        expected_operation_id="op-1",
        expected_action_name="bounded-write",
        expected_target_digest="target-v1",
        expected_effect_digest="effect-v1",
        expected_evidence_digest="evidence-v1",
        expected_context_digest="context-v1",
        current_authority_epoch=7,
    )


def test_fresh_context_bound_authority_is_allowed() -> None:
    result = _validate(_envelope())
    assert result.disposition is SecurityDisposition.ALLOW
    assert result.reasons == ()


def test_expired_authority_fails_closed() -> None:
    result = _validate(_envelope(expires_at=NOW))
    assert result.disposition is SecurityDisposition.HOLD
    assert "authority_expired" in result.reasons


def test_replayed_authority_for_other_operation_fails_closed() -> None:
    result = _validate(_envelope(operation_id="op-other"))
    assert result.disposition is SecurityDisposition.HOLD
    assert "authority_operation_mismatch" in result.reasons


def test_authority_is_bound_to_evidence_and_context() -> None:
    result = _validate(_envelope(evidence_digest="old-evidence", context_digest="old-context"))
    assert result.disposition is SecurityDisposition.HOLD
    assert set(result.reasons) == {"authority_evidence_mismatch", "authority_context_mismatch"}


def test_commit_authority_allows_exact_current_unconsumed_effect() -> None:
    result = _validate_commit(_commit_envelope())
    assert result.disposition is SecurityDisposition.ALLOW
    assert result.reasons == ()


def test_commit_authority_is_bound_to_exact_target_and_effect() -> None:
    result = _validate_commit(_commit_envelope(target_digest="target-old", effect_digest="effect-old"))
    assert result.disposition is SecurityDisposition.HOLD
    assert set(result.reasons) == {"commit_authority_target_mismatch", "commit_authority_effect_mismatch"}


def test_commit_authority_rejects_stale_epoch_after_revocation_or_regrant() -> None:
    result = _validate_commit(_commit_envelope(authority_epoch=6))
    assert result.disposition is SecurityDisposition.HOLD
    assert result.reasons == ("commit_authority_epoch_mismatch",)


def test_commit_authority_rejects_consumed_one_shot_authority() -> None:
    result = _validate_commit(_commit_envelope(consumed=True))
    assert result.disposition is SecurityDisposition.HOLD
    assert result.reasons == ("commit_authority_consumed",)


def test_commit_authority_rechecks_freshness_and_evidence_at_commit_time() -> None:
    result = _validate_commit(
        _commit_envelope(
            expires_at=NOW,
            evidence_digest="evidence-old",
            context_digest="context-old",
        )
    )
    assert result.disposition is SecurityDisposition.HOLD
    assert set(result.reasons) == {
        "commit_authority_expired",
        "commit_authority_evidence_mismatch",
        "commit_authority_context_mismatch",
    }


def test_integrity_snapshot_digest_is_deterministic_and_tamper_sensitive() -> None:
    original = ResponsibilityIntegritySnapshot(
        operation_id="op-1",
        state="human_gate",
        residual_owner="owner-a",
        human_return_point="review-desk",
        event_count=4,
        latest_event_digest="event-4",
    )
    same = ResponsibilityIntegritySnapshot(**original.__dict__)
    tampered = ResponsibilityIntegritySnapshot(
        operation_id="op-1",
        state="authorized",
        residual_owner="owner-a",
        human_return_point="review-desk",
        event_count=4,
        latest_event_digest="event-4",
    )
    assert original.canonical_digest() == same.canonical_digest()
    assert original.canonical_digest() != tampered.canonical_digest()


def test_non_equivocation_monitor_reports_conflicting_responsibility_views() -> None:
    left = ResponsibilityIntegritySnapshot(
        operation_id="op-1",
        state="effect_unknown",
        residual_owner="owner-a",
        human_return_point="review-desk",
        event_count=6,
        latest_event_digest="event-6-a",
    )
    right = ResponsibilityIntegritySnapshot(
        operation_id="op-1",
        state="completed",
        residual_owner="owner-b",
        human_return_point="other-desk",
        event_count=5,
        latest_event_digest="event-5-b",
    )
    codes = {finding.code for finding in find_responsibility_inconsistencies((left, right))}
    assert codes == {
        "responsibility_state_conflict",
        "residual_owner_conflict",
        "human_return_point_conflict",
        "event_history_length_conflict",
        "latest_event_digest_conflict",
    }


def test_non_equivocation_monitor_does_not_choose_a_winner() -> None:
    snapshot = ResponsibilityIntegritySnapshot(
        operation_id="op-1",
        state="effect_unknown",
        residual_owner="owner-a",
        human_return_point="review-desk",
        event_count=6,
        latest_event_digest="event-6",
    )
    assert find_responsibility_inconsistencies((snapshot, snapshot)) == ()
