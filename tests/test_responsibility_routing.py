# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path

from rpos import AdapterResult, OperationDefinition, OperationState, ReceiptStatus, RposService
from rpos.routing import ResponsibilityRouteKind, classify_responsibility_route


class FixedAdapter:
    def __init__(self, result: AdapterResult) -> None:
        self.result = result

    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        return self.result


def definition(operation_id: str, *, gate: bool = False) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name="bounded_external_write",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="approver" if gate else None,
        human_return_point="human-review",
        residual_owner="operator",
        resume_authority="resume-owner",
        requires_human_gate=gate,
        verification_required=True,
    )


def test_human_gate_routes_only_to_declared_approval_authority(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    inspection = service.propose(definition("op-gate", gate=True))

    route = classify_responsibility_route(inspection)

    assert route is not None
    assert route.route_kind is ResponsibilityRouteKind.HUMAN_GATE
    assert route.receiver == "approver"
    assert route.required_authority == "approver"
    assert route.authority_effect == "none"


def test_effect_unknown_prefers_reconciliation_not_automatic_human_return(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(definition("op-unknown"))
    inspection = service.dispatch(
        "op-unknown",
        attempt_id="a1",
        idempotency_key="k1",
        adapter=FixedAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {"accepted": True}, None, None)),
    )

    assert inspection.state is OperationState.EFFECT_UNKNOWN
    # Legacy inspection retains a HumanReturnPackage for compatibility.
    assert inspection.human_return is not None

    route = classify_responsibility_route(inspection)
    assert route is not None
    assert route.route_kind is ResponsibilityRouteKind.HOLD_FOR_RECONCILIATION
    assert route.receiver == "operator"
    assert route.authority_effect == "none"


def test_repair_and_resume_are_distinct_routes(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(definition("op-repair"))
    failed = service.dispatch(
        "op-repair",
        attempt_id="a1",
        idempotency_key="k1",
        adapter=FixedAdapter(AdapterResult(ReceiptStatus.FAILED, {}, False, {}, "write_failed")),
    )

    repair_route = classify_responsibility_route(failed)
    assert repair_route is not None
    assert repair_route.route_kind is ResponsibilityRouteKind.REPAIR
    assert repair_route.receiver == "operator"
    assert repair_route.required_authority == "operator"

    ready = service.prepare_repair("op-repair", actor="operator", summary="bounded repair prepared")
    resume_route = classify_responsibility_route(ready)
    assert resume_route is not None
    assert resume_route.route_kind is ResponsibilityRouteKind.RETURN_FOR_AUTHORIZATION
    assert resume_route.receiver == "resume-owner"
    assert resume_route.required_authority == "resume-owner"
    assert resume_route.authority_effect == "none"


def test_terminal_and_authorized_states_have_no_unresolved_route(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    authorized = service.propose(definition("op-complete"))
    assert authorized.state is OperationState.AUTHORIZED
    assert classify_responsibility_route(authorized) is None

    completed = service.dispatch(
        "op-complete",
        attempt_id="a1",
        idempotency_key="k1",
        adapter=FixedAdapter(AdapterResult(ReceiptStatus.SUCCEEDED, {}, True, {"exists": True})),
    )
    assert completed.state is OperationState.COMPLETED
    assert classify_responsibility_route(completed) is None
