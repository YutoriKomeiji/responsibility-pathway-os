# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from pathlib import Path

from rpos import OperationDefinition, RposService
from rpos.route_eligibility import assess_route_receiver
from rpos.route_assessment_history import (
    latest_recorded_route_assessment,
    record_route_assessment,
)
from rpos.routing import ResponsibilityRouteKind, classify_responsibility_route
from rpos.storage import SQLiteRposStore


def test_route_eligibility_history_survives_restart_without_restoring_authority(tmp_path: Path):
    db = str(tmp_path / "routing.db")
    svc = RposService(db)
    svc.propose(OperationDefinition(
        operation_id="op-restart", action_name="transfer", requested_by="user",
        execution_actor="agent", approval_authority="approver",
        human_return_point="reviewer", residual_owner="operator",
        requires_human_gate=True,
    ))
    store = SQLiteRposStore(db)
    route = classify_responsibility_route(svc.inspect("op-restart"))
    assert route is not None
    assessment = assess_route_receiver(
        route, authority_verified=True, delegation_verified=True,
        evidence_access_verified=True, intervention_capacity_verified=True,
        timing_verified=True, eligibility_basis="host evidence id: 1",
        residual_owner="operator",
    )
    record_route_assessment(store, assessment, actor="host-checker")
    store.connection.close()

    reopened = SQLiteRposStore(db)
    historical = latest_recorded_route_assessment(reopened, "op-restart")
    assert historical is not None
    assert historical.eligibility == "eligible"
    assert historical.effective_route == ResponsibilityRouteKind.HUMAN_GATE.value
    assert historical.residual_owner == "operator"
    # The historical record is NOT a live eligibility decision; changing host
    # delegation after restart must yield a neutral hold.
    current = assess_route_receiver(
        route, authority_verified=None, delegation_verified=None,
        evidence_access_verified=True, intervention_capacity_verified=True,
        timing_verified=True, eligibility_basis="old host evidence id: 1",
        residual_owner="operator",
    )
    assert current.permitted_to_transfer is False
    assert current.effective_route is ResponsibilityRouteKind.NEUTRAL_HOLD
    reopened.connection.close()
