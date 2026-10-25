# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
"""Conservative recipient eligibility assessment for a proposed responsibility route.

This is not an authorization service. The caller must supply independently
verified delegation/authority and evidence checks. Missing facts stay unknown.
"""
from __future__ import annotations

from dataclasses import dataclass
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
    if route.authority_effect != "none":
        raise ValueError("route selection must not create Authority")
    if any(v is False for v in checks):
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
    )
