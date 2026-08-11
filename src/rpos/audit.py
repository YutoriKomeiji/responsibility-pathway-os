# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Protocol

from .models import OperationInspection


class AuditEvidenceSource(Protocol):
    def inspect(self, operation_id: str) -> OperationInspection: ...

    def event_history(self, operation_id: str) -> list[dict[str, object]]: ...


_NOT_PROVEN = (
    "legal_or_regulatory_compliance",
    "general_ai_safety",
    "external_system_correctness",
    "supplier_or_dependency_trustworthiness",
    "software_supply_chain_conformance",
    "production_readiness",
    "real_world_effect_beyond_declared_readback",
)


def build_audit_evidence_package(source: AuditEvidenceSource, operation_id: str) -> dict[str, Any]:
    """Build a responsibility-oriented audit package without collapsing evidence classes."""

    inspection = source.inspect(operation_id)
    events = source.event_history(operation_id)

    authority: list[dict[str, object]] = []
    evaluation: list[dict[str, object]] = []
    dependency_supply_chain: list[dict[str, object]] = []
    execution: list[dict[str, object]] = []
    external_effect: list[dict[str, object]] = []
    recovery_resume: list[dict[str, object]] = []
    state_history: list[dict[str, object]] = []

    for event in events:
        event_type = str(event["event_type"])
        payload = event.get("payload")
        payload_dict = payload if isinstance(payload, dict) else {}

        if event_type == "operation_proposed":
            authority.append(event)
        elif event_type == "external_evaluation_evidence_recorded":
            evaluation.append(event)
        elif event_type == "dependency_evidence_recorded":
            dependency_supply_chain.append(event)
        elif event_type == "adapter_result":
            execution.append(event)
        elif event_type == "reconciliation_observed":
            external_effect.append(event)
        elif event_type == "repair_prepared":
            recovery_resume.append(event)
        elif event_type == "state_transition":
            state_history.append(event)
            reason = str(payload_dict.get("reason", ""))
            target = str(payload_dict.get("to", ""))
            if reason in {"initial_admission", "human_gate_approved"} or target == "denied":
                authority.append(event)
            elif target == "dispatching":
                execution.append(event)
            elif reason == "resume_authorized" or reason.startswith("restart_recovered_") or target == "ready_to_resume":
                recovery_resume.append(event)

    human_return = None if inspection.human_return is None else asdict(inspection.human_return)

    return {
        "schema_version": "rpos.audit.v0.1",
        "operation_id": operation_id,
        "current_state": inspection.state.value,
        "admission_decision": inspection.admission_decision.value,
        "operation_definition": inspection.definition.to_dict(),
        "evidence": {
            "authority_and_admission": authority,
            "evaluation": evaluation,
            "dependency_supply_chain": dependency_supply_chain,
            "execution_and_receipt": execution,
            "external_effect_readback": external_effect,
            "recovery_and_resume": recovery_resume,
        },
        "state_history": state_history,
        "unresolved_responsibility": human_return,
        "not_proven": list(_NOT_PROVEN),
    }
