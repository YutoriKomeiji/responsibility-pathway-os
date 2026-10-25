# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
"""Conservative recipient eligibility assessment for a proposed responsibility route.

This is not an authorization service. The caller must supply independently
verified delegation/authority and evidence checks. Missing facts stay unknown.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .routing import ResponsibilityRoute, ResponsibilityRouteKind


class ReceiverEligibility(StrEnum):
    ELIGIBLE = "eligible"
    INELIGIBLE = "ineligible"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class RouteEligibilityAssessment:
    proposed_route: ResponsibilityRoute
    eligibility: ReceiverEligibility
    effective_route: ResponsibilityRouteKind
    permitted_to_transfer: bool
    eligibility_basis: str
    residual_owner: str | None
    evidence_expires_at: datetime | None = None


def assess_route_receiver(
    route: ResponsibilityRoute,
    *,
    authority_verified: bool | None,
    delegation_verified: bool | None,
    evidence_access_verified: bool | None,
    intervention_capacity_verified: bool | None,
    timing_verified: bool | None,
    eligibility_basis: str = "",
    residual_owner: str | None = None,
    assessed_at: datetime | None = None,
    evidence_expires_at: datetime | None = None,
) -> RouteEligibilityAssessment:
    """Assess independently established facts; never infer Authority from names.

    A true result requires all five positive facts, an identified receiver and
    a nonempty external evidence basis. False means explicitly ineligible.
    Unknown means missing/unestablished facts. Noneligible routes are held,
    rather than automatically escalated to a human.
    """
    checks = (
        authority_verified,
        delegation_verified,
        evidence_access_verified,
        intervention_capacity_verified,
        timing_verified,
    )
    if (assessed_at is None) != (evidence_expires_at is None):
        raise ValueError("assessed_at and evidence_expires_at must be supplied together")
    if assessed_at is not None:
        if assessed_at.tzinfo is None or evidence_expires_at.tzinfo is None:
            raise ValueError("evidence timestamps must be timezone-aware")
    if route.authority_effect != "none":
        raise ValueError("route selection must not create Authority")
    if assessed_at is not None and assessed_at >= evidence_expires_at:
        eligibility = ReceiverEligibility.INELIGIBLE
    elif any(v is False for v in checks):
        eligibility = ReceiverEligibility.INELIGIBLE
    elif (route.receiver and all(v is True for v in checks)
          and eligibility_basis.strip()):
        eligibility = ReceiverEligibility.ELIGIBLE
    else:
        eligibility = ReceiverEligibility.UNKNOWN

    return RouteEligibilityAssessment(
        proposed_route=route,
        eligibility=eligibility,
        effective_route=(route.route_kind if eligibility is ReceiverEligibility.ELIGIBLE
                         else ResponsibilityRouteKind.NEUTRAL_HOLD),
        permitted_to_transfer=eligibility is ReceiverEligibility.ELIGIBLE,
        eligibility_basis=eligibility_basis,
        residual_owner=residual_owner,
        evidence_expires_at=evidence_expires_at,
    )
