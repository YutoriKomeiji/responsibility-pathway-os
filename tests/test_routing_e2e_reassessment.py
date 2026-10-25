# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
"""End-to-end bounded fixture: unknown external effect, eligibility, restart."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from rpos import AdapterResult, OperationDefinition, OperationState, ReceiptStatus, RposService
from rpos.route_assessment_history import latest_recorded_route_assessment, record_route_assessment
from rpos.route_eligibility import ReceiverEligibility, assess_route_receiver
from rpos.routing import ResponsibilityRouteKind, classify_responsibility_route
from rpos.storage import SQLiteRposStore


class AmbiguousWrite:
    calls = 0

    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str):
        self.calls += 1
        return AdapterResult(ReceiptStatus.SUCCEEDED, {"accepted": True}, None, None)


def test_unknown_effect_never_becomes_retry_or_cached_receiver_authority(tmp_path):
    db = str(tmp_path / "handoff.db")
    service = RposService(db)
    service.propose(OperationDefinition(
        operation_id="bounded-write", action_name="external_write",
        requested_by="requester", execution_actor="agent",
        approval_authority=None, human_return_point="human-review",
        residual_owner="operator", verification_required=True,
    ))
    adapter = AmbiguousWrite()
    unknown = service.dispatch(
        "bounded-write", attempt_id="attempt-1", idempotency_key="key-1",
        adapter=adapter,
    )
    assert unknown.state is OperationState.EFFECT_UNKNOWN
    route = classify_responsibility_route(unknown)
    assert route is not None
    assert route.route_kind is ResponsibilityRouteKind.HOLD_FOR_RECONCILIATION

    now = datetime(2026, 10, 26, tzinfo=timezone.utc)
    valid = assess_route_receiver(
        route, authority_verified=True, delegation_verified=True,
        evidence_access_verified=True, intervention_capacity_verified=True,
        timing_verified=True, eligibility_basis="host-readback-authorization-1",
        residual_owner="operator", assessed_at=now,
        evidence_expires_at=now + timedelta(minutes=5),
    )
    assert valid.permitted_to_transfer
    assert valid.effective_route is ResponsibilityRouteKind.HOLD_FOR_RECONCILIATION

    store = SQLiteRposStore(db)
    record_route_assessment(store, valid, actor="host-fixture")
    store.connection.close()

    rebooted = RposService(db)
    observed = rebooted.inspect("bounded-write")
    assert observed.state is OperationState.EFFECT_UNKNOWN
    historical_store = SQLiteRposStore(db)
    historical = latest_recorded_route_assessment(historical_store, "bounded-write")
    assert historical is not None and historical.eligibility == "eligible"

    # The stored positive assessment has expired. Neither restarting the
    # process nor having once been eligible authorizes another write.
    held = assess_route_receiver(
        classify_responsibility_route(observed),
        authority_verified=True, delegation_verified=True,
        evidence_access_verified=True, intervention_capacity_verified=True,
        timing_verified=True, eligibility_basis="host-readback-authorization-1",
        residual_owner="operator", assessed_at=now + timedelta(minutes=5),
        evidence_expires_at=now + timedelta(minutes=5),
    )
    assert held.eligibility is ReceiverEligibility.INELIGIBLE
    assert not held.permitted_to_transfer
    assert held.effective_route is ResponsibilityRouteKind.NEUTRAL_HOLD
    assert adapter.calls == 1
    historical_store.connection.close()
