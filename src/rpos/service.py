# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import asdict

from .adapters import OperationAdapter, ReconciliationObserver
from .dependency import DependencyEvidence
from .evidence import ExternalEvaluationEvidence
from .models import (
    AdmissionDecision,
    AdapterResult,
    BootReport,
    HumanReturnPackage,
    OperationDefinition,
    OperationInspection,
    OperationState,
    ReceiptStatus,
    ReconciliationResult,
    ReconciliationStatus,
)
from .security import ResponsibilityEventChainCheckpoint, build_event_chain_checkpoint
from .storage import SQLiteRposStore


_ALLOWED: dict[OperationState, set[OperationState]] = {
    OperationState.PROPOSED: {OperationState.HUMAN_GATE, OperationState.AUTHORIZED, OperationState.DENIED},
    OperationState.HUMAN_GATE: {OperationState.AUTHORIZED, OperationState.DENIED},
    OperationState.AUTHORIZED: {OperationState.DISPATCHING},
    OperationState.DISPATCHING: {
        OperationState.VERIFIED,
        OperationState.EFFECT_UNKNOWN,
        OperationState.REPAIR_REQUIRED,
    },
    OperationState.EFFECT_UNKNOWN: {OperationState.VERIFIED, OperationState.REPAIR_REQUIRED},
    OperationState.VERIFIED: {OperationState.COMPLETED},
    OperationState.REPAIR_REQUIRED: {OperationState.READY_TO_RESUME},
    OperationState.READY_TO_RESUME: {OperationState.AUTHORIZED},
    OperationState.COMPLETED: set(),
    OperationState.DENIED: set(),
    OperationState.ABORTED: set(),
}

_UNRESOLVED = {
    OperationState.HUMAN_GATE,
    OperationState.DISPATCHING,
    OperationState.EFFECT_UNKNOWN,
    OperationState.REPAIR_REQUIRED,
    OperationState.READY_TO_RESUME,
}


def classify_adapter_result(definition: OperationDefinition, result: AdapterResult) -> OperationState:
    if result.receipt_status is ReceiptStatus.FAILED:
        return OperationState.REPAIR_REQUIRED
    if result.receipt_status is ReceiptStatus.SUCCEEDED:
        if definition.verification_required:
            return OperationState.VERIFIED if result.readback_verified is True else OperationState.EFFECT_UNKNOWN
        return OperationState.VERIFIED
    return OperationState.EFFECT_UNKNOWN


class RposService:
    def __init__(self, database_path: str = ":memory:") -> None:
        self.store = SQLiteRposStore(database_path)

    def boot_report(self) -> BootReport:
        return BootReport(
            schema_available=True,
            operation_count=self.store.count_operations(),
            unresolved_operation_ids=tuple(self.list_unresolved()),
        )

    def propose(self, definition: OperationDefinition) -> OperationInspection:
        decision = AdmissionDecision.HUMAN_GATE if definition.requires_human_gate else AdmissionDecision.ALLOW
        target = OperationState.HUMAN_GATE if decision is AdmissionDecision.HUMAN_GATE else OperationState.AUTHORIZED
        with self.store.transaction():
            self.store.create_operation(definition, OperationState.PROPOSED, decision)
            self.store.record_event(
                definition.operation_id,
                "operation_proposed",
                definition.requested_by,
                {"definition": definition.to_dict(), "admission_decision": decision.value},
            )
            self._transition(definition.operation_id, target, actor=definition.requested_by, reason="initial_admission")
        return self.inspect(definition.operation_id)

    def record_evaluation_evidence(
        self,
        operation_id: str,
        *,
        actor: str,
        evidence: ExternalEvaluationEvidence,
    ) -> OperationInspection:
        if not actor.strip():
            raise ValueError("actor must not be empty")
        self.store.get_operation(operation_id)
        self.store.record_event(
            operation_id,
            "external_evaluation_evidence_recorded",
            actor,
            {"evidence": evidence.to_dict()},
        )
        return self.inspect(operation_id)

    def record_dependency_evidence(
        self,
        operation_id: str,
        *,
        actor: str,
        evidence: DependencyEvidence,
    ) -> OperationInspection:
        if not actor.strip():
            raise ValueError("actor must not be empty")
        self.store.get_operation(operation_id)
        self.store.record_event(
            operation_id,
            "dependency_evidence_recorded",
            actor,
            {"evidence": evidence.to_dict()},
        )
        return self.inspect(operation_id)

    def approve(self, operation_id: str, *, actor: str) -> OperationInspection:
        definition, state, _ = self.store.get_operation(operation_id)
        if state is not OperationState.HUMAN_GATE:
            raise ValueError(f"operation is not awaiting Human Gate approval: {state.value}")
        if actor != definition.approval_authority:
            raise PermissionError("actor is not the declared approval authority")
        self._transition(operation_id, OperationState.AUTHORIZED, actor=actor, reason="human_gate_approved")
        return self.inspect(operation_id)

    def deny(self, operation_id: str, *, actor: str, reason: str) -> OperationInspection:
        definition, state, _ = self.store.get_operation(operation_id)
        if state is not OperationState.HUMAN_GATE:
            raise ValueError(f"operation is not awaiting Human Gate decision: {state.value}")
        if actor != definition.approval_authority:
            raise PermissionError("actor is not the declared approval authority")
        self._transition(operation_id, OperationState.DENIED, actor=actor, reason=reason)
        return self.inspect(operation_id)

    def dispatch(
        self,
        operation_id: str,
        *,
        attempt_id: str,
        idempotency_key: str,
        adapter: OperationAdapter,
    ) -> OperationInspection:
        definition, state, _ = self.store.get_operation(operation_id)
        prior = self.store.get_attempt_by_idempotency_key(operation_id, idempotency_key)
        if prior is not None:
            return self.inspect(operation_id)
        if state is not OperationState.AUTHORIZED:
            raise PermissionError(f"operation is not authorized for dispatch: {state.value}")

        # Persist the attempt and DISPATCHING transition atomically before any
        # external effect. A crash before commit leaves the operation authorized;
        # a crash after commit leaves a recoverable DISPATCHING responsibility.
        with self.store.transaction():
            self.store.begin_attempt(operation_id, attempt_id, idempotency_key)
            self._transition(
                operation_id,
                OperationState.DISPATCHING,
                actor=definition.execution_actor,
                reason=f"dispatch_started:{attempt_id}",
            )

        try:
            result = adapter.execute(
                operation_id=operation_id,
                attempt_id=attempt_id,
                idempotency_key=idempotency_key,
            )
        except Exception as exc:
            result = AdapterResult(
                receipt_status=ReceiptStatus.UNKNOWN,
                receipt={},
                readback_verified=None,
                readback=None,
                reason=f"adapter_exception:{type(exc).__name__}",
            )

        target = classify_adapter_result(definition, result)
        # Persist receipt metadata, evidence event, and resulting state in one
        # transaction. If this transaction is interrupted, restart recovery sees
        # DISPATCHING and must not redispatch automatically.
        with self.store.transaction():
            self.store.finish_attempt(
                attempt_id,
                receipt_status=result.receipt_status.value,
                readback_verified=result.readback_verified,
                result_reason=result.reason,
            )
            self.store.record_event(
                operation_id,
                "adapter_result",
                definition.execution_actor,
                {
                    "attempt_id": attempt_id,
                    "idempotency_key": idempotency_key,
                    "result": asdict(result),
                },
            )
            self._transition(
                operation_id,
                target,
                actor=definition.execution_actor,
                reason=result.reason or "adapter_result_classified",
            )
            if target is OperationState.VERIFIED:
                self._transition(
                    operation_id,
                    OperationState.COMPLETED,
                    actor=definition.execution_actor,
                    reason="verified_effect_completed",
                )
        return self.inspect(operation_id)

    def reconcile(
        self,
        operation_id: str,
        *,
        actor: str,
        observer: ReconciliationObserver,
    ) -> OperationInspection:
        definition, state, _ = self.store.get_operation(operation_id)
        if state is not OperationState.EFFECT_UNKNOWN:
            raise ValueError(f"operation is not in effect_unknown: {state.value}")
        if actor != definition.residual_owner:
            raise PermissionError("actor is not the declared residual owner")

        latest_attempt = self.store.latest_attempt(operation_id)
        try:
            result = observer.observe(operation_id=operation_id, latest_attempt=latest_attempt)
        except Exception as exc:
            result = ReconciliationResult(
                status=ReconciliationStatus.UNRESOLVED,
                evidence={},
                reason=f"reconciliation_exception:{type(exc).__name__}",
            )

        if result.status is ReconciliationStatus.VERIFIED_APPLIED and not result.evidence:
            raise ValueError("verified_applied reconciliation requires evidence")
        if result.status not in {
            ReconciliationStatus.VERIFIED_APPLIED,
            ReconciliationStatus.VERIFIED_NOT_APPLIED,
            ReconciliationStatus.UNRESOLVED,
        }:
            raise ValueError(f"unsupported reconciliation status: {result.status}")

        with self.store.transaction():
            self.store.record_event(
                operation_id,
                "reconciliation_observed",
                actor,
                {
                    "attempt_id": None if latest_attempt is None else latest_attempt.get("attempt_id"),
                    "status": result.status.value,
                    "evidence": dict(result.evidence),
                    "reason": result.reason,
                },
            )

            if result.status is ReconciliationStatus.VERIFIED_APPLIED:
                self._transition(
                    operation_id,
                    OperationState.VERIFIED,
                    actor=actor,
                    reason=result.reason or "reconciliation_verified_applied",
                )
                self._transition(
                    operation_id,
                    OperationState.COMPLETED,
                    actor=actor,
                    reason="reconciled_effect_completed",
                )
            elif result.status is ReconciliationStatus.VERIFIED_NOT_APPLIED:
                self._transition(
                    operation_id,
                    OperationState.REPAIR_REQUIRED,
                    actor=actor,
                    reason=result.reason or "reconciliation_verified_not_applied",
                )

        return self.inspect(operation_id)

    def prepare_repair(self, operation_id: str, *, actor: str, summary: str) -> OperationInspection:
        definition, state, _ = self.store.get_operation(operation_id)
        if state is not OperationState.REPAIR_REQUIRED:
            raise ValueError(f"operation is not repair-required: {state.value}")
        if actor != definition.residual_owner:
            raise PermissionError("actor is not the declared residual owner")
        if not summary.strip():
            raise ValueError("repair summary must not be empty")

        latest_attempt = self.store.latest_attempt(operation_id)
        with self.store.transaction():
            self.store.record_event(
                operation_id,
                "repair_prepared",
                actor,
                {
                    "attempt_id": None if latest_attempt is None else latest_attempt.get("attempt_id"),
                    "summary": summary.strip(),
                },
            )
            self._transition(operation_id, OperationState.READY_TO_RESUME, actor=actor, reason="repair_prepared")
        return self.inspect(operation_id)

    def resume(self, operation_id: str, *, actor: str) -> OperationInspection:
        definition, state, _ = self.store.get_operation(operation_id)
        if state is not OperationState.READY_TO_RESUME:
            raise ValueError(f"operation is not ready to resume: {state.value}")
        if actor != definition.effective_resume_authority:
            raise PermissionError("actor is not the declared resume authority")
        self._transition(operation_id, OperationState.AUTHORIZED, actor=actor, reason="resume_authorized")
        return self.inspect(operation_id)

    def recover_incomplete_dispatches(self) -> tuple[str, ...]:
        recovered: list[str] = []
        for operation_id in self.store.dispatching_operations():
            definition, state, _ = self.store.get_operation(operation_id)
            if state is not OperationState.DISPATCHING:
                continue
            self._transition(
                operation_id,
                OperationState.EFFECT_UNKNOWN,
                actor=definition.residual_owner,
                reason="restart_recovered_incomplete_dispatch_without_redispatch",
            )
            recovered.append(operation_id)
        return tuple(recovered)

    def list_unresolved(self) -> list[str]:
        return self.store.list_by_states(_UNRESOLVED)

    def event_history(self, operation_id: str) -> list[dict[str, object]]:
        return self.store.list_events(operation_id)

    def event_chain_checkpoint(self, operation_id: str) -> ResponsibilityEventChainCheckpoint:
        """Return a tamper-sensitive checkpoint for the complete observed event history."""
        return build_event_chain_checkpoint(operation_id, self.store.list_events(operation_id))

    def inspect(self, operation_id: str) -> OperationInspection:
        definition, state, decision = self.store.get_operation(operation_id)
        latest_attempt = self.store.latest_attempt(operation_id)
        human_return = None
        if state in _UNRESOLVED:
            if state is OperationState.HUMAN_GATE:
                required_authority = definition.approval_authority
                unresolved_reason = "human_gate_decision_required"
            elif state is OperationState.REPAIR_REQUIRED:
                required_authority = definition.residual_owner
                unresolved_reason = "repair_required"
            elif state is OperationState.READY_TO_RESUME:
                required_authority = definition.effective_resume_authority
                unresolved_reason = "resume_authorization_required"
            elif state in {OperationState.DISPATCHING, OperationState.EFFECT_UNKNOWN}:
                required_authority = definition.residual_owner
                unresolved_reason = "external_effect_not_verified"
            else:
                required_authority = definition.residual_owner
                unresolved_reason = "unresolved"
            human_return = HumanReturnPackage(
                operation_id=operation_id,
                state=state,
                human_return_point=definition.human_return_point,
                residual_owner=definition.residual_owner,
                required_authority=required_authority,
                summary=f"Operation {operation_id} requires responsible review in state {state.value}.",
                unresolved_reason=unresolved_reason,
            )
        return OperationInspection(definition, state, decision, latest_attempt, human_return)

    def _transition(self, operation_id: str, target: OperationState, *, actor: str, reason: str) -> None:
        # State and its transition event are one durable fact. Nested calls join
        # an outer service transaction; standalone transitions commit atomically.
        with self.store.transaction():
            _, current, _ = self.store.get_operation(operation_id)
            if target not in _ALLOWED[current]:
                raise ValueError(f"invalid transition: {current.value} -> {target.value}")
            self.store.set_state(operation_id, target)
            self.store.record_event(
                operation_id,
                "state_transition",
                actor,
                {"from": current.value, "to": target.value, "reason": reason},
            )
