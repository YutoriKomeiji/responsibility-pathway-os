# Copyright (c) 2026 RPOS contributors
# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path

import pytest

from rpos import (
    DependencyEvidence,
    DependencyEvidenceClass,
    OperationDefinition,
    OperationState,
    RposService,
    build_audit_evidence_package,
)


def _gated_definition(operation_id: str) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name="bounded_external_operation",
        requested_by="requester",
        execution_actor="executor",
        approval_authority="human_authority",
        human_return_point="human-authority-review",
        residual_owner="operator",
        resume_authority="human_authority",
        requires_human_gate=True,
        verification_required=True,
    )


def _evidence() -> DependencyEvidence:
    return DependencyEvidence(
        evidence_id="dependency-001",
        evidence_class=DependencyEvidenceClass.ADAPTER,
        source_system="software-inventory",
        source_reference="adapter-record-001",
        source_revision="rev-7",
        component_name="bounded-adapter",
        component_version="0.1.0",
        dependency_owner="dependency_owner",
        verification_method="digest-and-source-revision",
        artifact_digest="sha256:example",
        supplier_role="adapter_provider",
        unresolved_risk="external service behavior remains independently verifiable",
    )


def test_dependency_evidence_does_not_authorize_or_dispatch(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    proposed = service.propose(_gated_definition("dependency-evidence-001"))
    assert proposed.state is OperationState.HUMAN_GATE

    recorded = service.record_dependency_evidence(
        "dependency-evidence-001",
        actor="evidence_producer",
        evidence=_evidence(),
    )

    assert recorded.state is OperationState.HUMAN_GATE
    assert recorded.latest_attempt is None
    with pytest.raises(PermissionError):
        service.dispatch(
            "dependency-evidence-001",
            attempt_id="attempt-1",
            idempotency_key="dispatch-1",
            adapter=object(),  # type: ignore[arg-type]
        )


def test_dependency_import_rejects_unexpected_fields() -> None:
    payload = _evidence().to_dict()
    payload["raw_environment"] = "must-not-enter-event-history"

    with pytest.raises(ValueError, match="unexpected fields"):
        DependencyEvidence.from_import_dict(payload)


def test_dependency_evidence_is_separate_in_audit_package(tmp_path: Path) -> None:
    service = RposService(str(tmp_path / "rpos.db"))
    service.propose(_gated_definition("dependency-evidence-002"))
    service.record_dependency_evidence(
        "dependency-evidence-002",
        actor="evidence_producer",
        evidence=_evidence(),
    )

    package = build_audit_evidence_package(service, "dependency-evidence-002")
    dependency_events = package["evidence"]["dependency_supply_chain"]

    assert len(dependency_events) == 1
    assert package["current_state"] == "human_gate"
    assert package["evidence"]["execution_and_receipt"] == []
    assert "supplier_or_dependency_trustworthiness" in package["not_proven"]
    assert "software_supply_chain_conformance" in package["not_proven"]
