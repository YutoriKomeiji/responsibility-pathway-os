# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .models import AdmissionDecision, OperationState

if TYPE_CHECKING:
    from .service import RposService


@dataclass(frozen=True)
class ResponsibilityObservation:
    """Read-only product projection of one responsibility pathway.

    ``allowed_next_actions`` is explanatory guidance derived from the current
    state. It is not authorization. Mutation APIs remain responsible for all
    authority, state-transition, and evidence checks.
    """

    operation_id: str
    action_name: str
    state: OperationState
    admission_decision: AdmissionDecision
    residual_owner: str
    human_return_point: str
    required_authority: str | None
    unresolved_reason: str | None
    allowed_next_actions: tuple[str, ...]
    event_count: int


_NEXT_ACTION_GUIDANCE: dict[OperationState, tuple[str, ...]] = {
    OperationState.PROPOSED: ("await_admission",),
    OperationState.HUMAN_GATE: ("human_gate_decision",),
    OperationState.AUTHORIZED: ("dispatch",),
    OperationState.DISPATCHING: ("observe_external_effect",),
    OperationState.EFFECT_UNKNOWN: ("reconcile",),
    OperationState.VERIFIED: ("complete_after_verified_effect",),
    OperationState.REPAIR_REQUIRED: ("prepare_repair",),
    OperationState.READY_TO_RESUME: ("request_resume_authorization",),
    OperationState.COMPLETED: (),
    OperationState.DENIED: (),
    OperationState.ABORTED: (),
}


class ResponsibilityObservatory:
    """Observation-only facade over an ``RposService``.

    This facade intentionally exposes no mutating operation. Calling
    :meth:`observe` uses only existing inspection/history reads and does not
    record a new observation event. That property is checked by executable
    tests; the separate Lean teaching model states the abstract boundary.
    """

    def __init__(self, service: RposService) -> None:
        self._service = service

    def observe(self, operation_id: str) -> ResponsibilityObservation:
        before = self._service.inspect(operation_id)
        events = self._service.event_history(operation_id)
        human_return = before.human_return
        return ResponsibilityObservation(
            operation_id=before.definition.operation_id,
            action_name=before.definition.action_name,
            state=before.state,
            admission_decision=before.admission_decision,
            residual_owner=before.definition.residual_owner,
            human_return_point=before.definition.human_return_point,
            required_authority=None if human_return is None else human_return.required_authority,
            unresolved_reason=None if human_return is None else human_return.unresolved_reason,
            allowed_next_actions=_NEXT_ACTION_GUIDANCE[before.state],
            event_count=len(events),
        )
