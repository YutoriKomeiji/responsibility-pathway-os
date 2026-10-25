# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
"""Persist historical route assessment evidence without restoring authority."""
from __future__ import annotations

from dataclasses import dataclass

from .route_eligibility import RouteEligibilityAssessment
from .storage import SQLiteRposStore

_EVENT = "route_eligibility_observed"


@dataclass(frozen=True)
class RecordedRouteAssessment:
    operation_id: str
    eligibility: str
    proposed_route: str
    effective_route: str
    receiver: str | None
    residual_owner: str | None
    eligibility_basis: str
    event_seq: int


def record_route_assessment(
    store: SQLiteRposStore,
    assessment: RouteEligibilityAssessment,
    *,
    actor: str,
) -> None:
    """Record an observation, never an enduring approval or transfer grant."""
    if not actor.strip():
        raise ValueError("actor is required")
    route = assessment.proposed_route
    store.record_event(
        route.operation_id,
        _EVENT,
        actor,
        {
            "eligibility": assessment.eligibility.value,
            "proposed_route": route.route_kind.value,
            "effective_route": assessment.effective_route.value,
            "receiver": route.receiver,
            "residual_owner": assessment.residual_owner,
            "eligibility_basis": assessment.eligibility_basis,
            "historical_only": True,
            "authority_effect": "none",
        },
    )


def latest_recorded_route_assessment(
    store: SQLiteRposStore, operation_id: str
) -> RecordedRouteAssessment | None:
    """Read history after restart; caller MUST independently re-assess eligibility."""
    events = store.list_events(operation_id)
    records = [e for e in events if e["event_type"] == _EVENT]
    if not records:
        return None
    event = records[-1]
    value = event["payload"]
    if value.get("historical_only") is not True or value.get("authority_effect") != "none":
        raise ValueError("route assessment event cannot be interpreted as authority")
    return RecordedRouteAssessment(
        operation_id=operation_id,
        eligibility=str(value["eligibility"]),
        proposed_route=str(value["proposed_route"]),
        effective_route=str(value["effective_route"]),
        receiver=value.get("receiver"),
        residual_owner=value.get("residual_owner"),
        eligibility_basis=str(value.get("eligibility_basis", "")),
        event_seq=int(event["seq"]),
    )
