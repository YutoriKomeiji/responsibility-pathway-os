# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .models import OperationInspection, OperationState


class ResponsibilityRouteKind(StrEnum):
    """Bounded routing outcomes for unresolved responsibility state.

    These route kinds do not create Authority. They describe where an already
    unresolved operation should go next while preserving the current v0.1
    operation-state contract.
    """

    HUMAN_GATE = "human_gate"
    HOLD_FOR_RECONCILIATION = "hold_for_reconciliation"
    REPAIR = "repair"
    RETURN_FOR_AUTHORIZATION = "return_for_authorization"
    NEUTRAL_HOLD = "neutral_hold"


@dataclass(frozen=True)
class ResponsibilityRoute:
    operation_id: str
    state: OperationState
    route_kind: ResponsibilityRouteKind
    receiver: str | None
    required_authority: str | None
    authority_effect: str
    reason: str


def classify_responsibility_route(inspection: OperationInspection) -> ResponsibilityRoute | None:
    """Classify the next bounded route without changing operation state.

    Important boundaries:
    - route selection does not grant or transfer Authority;
    - Human Return is not inferred merely because an operation is unresolved;
    - effect uncertainty stays in a reconciliation route until evidence or an
      authorized decision changes the path;
    - repair completion does not imply resume Authority.
    """

    definition = inspection.definition
    state = inspection.state

    if state is OperationState.HUMAN_GATE:
        return ResponsibilityRoute(
            operation_id=definition.operation_id,
            state=state,
            route_kind=ResponsibilityRouteKind.HUMAN_GATE,
            receiver=definition.approval_authority,
            required_authority=definition.approval_authority,
            authority_effect="none",
            reason="declared_approval_authority_required",
        )

    if state in {OperationState.DISPATCHING, OperationState.EFFECT_UNKNOWN}:
        return ResponsibilityRoute(
            operation_id=definition.operation_id,
            state=state,
            route_kind=ResponsibilityRouteKind.HOLD_FOR_RECONCILIATION,
            receiver=definition.residual_owner,
            required_authority=definition.residual_owner,
            authority_effect="none",
            reason="external_effect_requires_reconciliation_before_retry_or_completion",
        )

    if state is OperationState.REPAIR_REQUIRED:
        return ResponsibilityRoute(
            operation_id=definition.operation_id,
            state=state,
            route_kind=ResponsibilityRouteKind.REPAIR,
            receiver=definition.residual_owner,
            required_authority=definition.residual_owner,
            authority_effect="none",
            reason="repair_required_under_existing_residual_ownership",
        )

    if state is OperationState.READY_TO_RESUME:
        return ResponsibilityRoute(
            operation_id=definition.operation_id,
            state=state,
            route_kind=ResponsibilityRouteKind.RETURN_FOR_AUTHORIZATION,
            receiver=definition.effective_resume_authority,
            required_authority=definition.effective_resume_authority,
            authority_effect="none",
            reason="repair_readiness_requires_existing_resume_authority",
        )

    return None
