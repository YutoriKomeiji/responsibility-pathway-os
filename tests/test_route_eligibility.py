# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from rpos.models import OperationState
from rpos.routing import ResponsibilityRoute, ResponsibilityRouteKind
from rpos.route_eligibility import ReceiverEligibility, assess_route_receiver


def _route(kind=ResponsibilityRouteKind.HOLD_FOR_RECONCILIATION):
    return ResponsibilityRoute(
        operation_id="op-1", state=OperationState.EFFECT_UNKNOWN,
        route_kind=kind, receiver="reconciler", required_authority="readback",
        authority_effect="none", reason="external_effect_unknown",
    )


def _assess(route=None, **overrides):
    args = dict(
        authority_verified=True, delegation_verified=True,
        evidence_access_verified=True, intervention_capacity_verified=True,
        timing_verified=True, eligibility_basis="verified host delegation record",
        residual_owner="operator",
    )
    args.update(overrides)
    return assess_route_receiver(route or _route(), **args)


def test_all_verified_facts_allow_only_the_existing_proposed_route():
    result = _assess()
    assert result.eligibility is ReceiverEligibility.ELIGIBLE
    assert result.permitted_to_transfer is True
    assert result.effective_route is ResponsibilityRouteKind.HOLD_FOR_RECONCILIATION
    assert result.proposed_route.authority_effect == "none"
    assert result.residual_owner == "operator"


def test_missing_evidence_does_not_infer_eligibility_or_human_return():
    result = _assess(delegation_verified=None)
    assert result.eligibility is ReceiverEligibility.UNKNOWN
    assert result.permitted_to_transfer is False
    assert result.effective_route is ResponsibilityRouteKind.NEUTRAL_HOLD


def test_explicit_ineligibility_holds_even_if_all_other_facts_pass():
    result = _assess(evidence_access_verified=False)
    assert result.eligibility is ReceiverEligibility.INELIGIBLE
    assert result.effective_route is ResponsibilityRouteKind.NEUTRAL_HOLD


def test_receiver_name_and_claimed_capability_are_not_sufficient():
    route = _route()
    result = _assess(route, eligibility_basis="")
    assert result.eligibility is ReceiverEligibility.UNKNOWN
    assert result.permitted_to_transfer is False


def test_even_human_gate_target_requires_verified_receiver():
    result = _assess(_route(ResponsibilityRouteKind.HUMAN_GATE),
                     authority_verified=None)
    assert result.effective_route is ResponsibilityRouteKind.NEUTRAL_HOLD
    assert result.permitted_to_transfer is False


def test_route_selection_must_not_grant_authority():
    bad = ResponsibilityRoute(
        operation_id="op-1", state=OperationState.EFFECT_UNKNOWN,
        route_kind=ResponsibilityRouteKind.HUMAN_GATE,
        receiver="reviewer", required_authority="approval",
        authority_effect="grant", reason="bad-route",
    )
    import pytest
    with pytest.raises(ValueError, match="must not create Authority"):
        _assess(bad)


def test_expired_route_evidence_does_not_allow_transfer():
    now = datetime(2026, 10, 25, tzinfo=timezone.utc)
    result = _assess(assessed_at=now, evidence_expires_at=now)
    assert result.eligibility is ReceiverEligibility.INELIGIBLE
    assert result.permitted_to_transfer is False
    assert result.effective_route is ResponsibilityRouteKind.NEUTRAL_HOLD


def test_unexpired_route_evidence_keeps_existing_eligibility_logic():
    now = datetime(2026, 10, 25, tzinfo=timezone.utc)
    result = _assess(assessed_at=now, evidence_expires_at=now + timedelta(minutes=5))
    assert result.eligibility is ReceiverEligibility.ELIGIBLE
    assert result.evidence_expires_at == now + timedelta(minutes=5)


def test_partial_or_naive_expiry_inputs_are_rejected():
    import pytest
    now = datetime(2026, 10, 25, tzinfo=timezone.utc)
    with pytest.raises(ValueError, match="supplied together"):
        _assess(assessed_at=now)
    with pytest.raises(ValueError, match="timezone-aware"):
        _assess(assessed_at=now, evidence_expires_at=datetime(2026, 10, 26))
