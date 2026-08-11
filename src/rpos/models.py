# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class OperationState(StrEnum):
    PROPOSED = "proposed"
    HUMAN_GATE = "human_gate"
    AUTHORIZED = "authorized"
    DISPATCHING = "dispatching"
    EFFECT_UNKNOWN = "effect_unknown"
    VERIFIED = "verified"
    REPAIR_REQUIRED = "repair_required"
    READY_TO_RESUME = "ready_to_resume"
    COMPLETED = "completed"
    DENIED = "denied"
    ABORTED = "aborted"


class AdmissionDecision(StrEnum):
    ALLOW = "allow"
    HUMAN_GATE = "human_gate"
    DENY = "deny"


class ReceiptStatus(StrEnum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    UNKNOWN = "unknown"


class ReconciliationStatus(StrEnum):
    VERIFIED_APPLIED = "verified_applied"
    VERIFIED_NOT_APPLIED = "verified_not_applied"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class OperationDefinition:
    operation_id: str
    action_name: str
    requested_by: str
    execution_actor: str
    approval_authority: str | None
    human_return_point: str
    residual_owner: str
    resume_authority: str | None = None
    requires_human_gate: bool = False
    verification_required: bool = True

    def __post_init__(self) -> None:
        for name in (
            "operation_id",
            "action_name",
            "requested_by",
            "execution_actor",
            "human_return_point",
            "residual_owner",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if self.requires_human_gate and not self.approval_authority:
            raise ValueError("approval_authority is required when requires_human_gate is true")
        if self.resume_authority is not None and not self.resume_authority.strip():
            raise ValueError("resume_authority must not be empty when supplied")

    @property
    def effective_resume_authority(self) -> str:
        return self.resume_authority or self.residual_owner

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "OperationDefinition":
        residual_owner = str(value["residual_owner"])
        return cls(
            operation_id=str(value["operation_id"]),
            action_name=str(value["action_name"]),
            requested_by=str(value["requested_by"]),
            execution_actor=str(value["execution_actor"]),
            approval_authority=value.get("approval_authority"),
            human_return_point=str(value["human_return_point"]),
            residual_owner=residual_owner,
            resume_authority=value.get("resume_authority") or residual_owner,
            requires_human_gate=bool(value.get("requires_human_gate", False)),
            verification_required=bool(value.get("verification_required", True)),
        )


@dataclass(frozen=True)
class AdapterResult:
    receipt_status: ReceiptStatus
    receipt: dict[str, Any]
    readback_verified: bool | None = None
    readback: dict[str, Any] | None = None
    reason: str | None = None


@dataclass(frozen=True)
class ReconciliationResult:
    status: ReconciliationStatus
    evidence: dict[str, Any]
    reason: str | None = None


@dataclass(frozen=True)
class BootReport:
    schema_available: bool
    operation_count: int
    unresolved_operation_ids: tuple[str, ...]


@dataclass(frozen=True)
class HumanReturnPackage:
    operation_id: str
    state: OperationState
    human_return_point: str
    residual_owner: str
    required_authority: str | None
    summary: str
    unresolved_reason: str | None


@dataclass(frozen=True)
class OperationInspection:
    definition: OperationDefinition
    state: OperationState
    admission_decision: AdmissionDecision
    latest_attempt: dict[str, Any] | None
    human_return: HumanReturnPackage | None
