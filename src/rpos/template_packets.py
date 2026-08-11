# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping


class PacketTemplateKind(StrEnum):
    OPERATION_PROPOSAL = "operation_proposal"
    HUMAN_GATE_DECISION = "human_gate_decision"
    VERIFICATION_CONTRACT = "verification_contract"
    REPAIR_PLAN = "repair_plan"
    RESUME_AUTHORIZATION = "resume_authorization"
    DEPENDENCY_EVIDENCE = "dependency_evidence"
    EXTERNAL_EVALUATION_EVIDENCE = "external_evaluation_evidence"
    HUMAN_RETURN_PACKET = "human_return_packet"


_REQUIRED: dict[PacketTemplateKind, frozenset[str]] = {
    PacketTemplateKind.OPERATION_PROPOSAL: frozenset({
        "operation_id", "action_name", "requested_by", "execution_actor",
        "approval_authority", "residual_owner", "human_return_point",
        "verification_required",
    }),
    PacketTemplateKind.HUMAN_GATE_DECISION: frozenset({
        "operation_id", "decision", "decision_actor", "decision_reason",
    }),
    PacketTemplateKind.VERIFICATION_CONTRACT: frozenset({
        "contract_id", "operation_id", "effect_description", "observer_role",
        "evidence_required", "unresolved_classification",
    }),
    PacketTemplateKind.REPAIR_PLAN: frozenset({
        "operation_id", "repair_owner", "failure_or_uncertainty", "repair_action",
        "readiness_evidence", "human_return_point",
    }),
    PacketTemplateKind.RESUME_AUTHORIZATION: frozenset({
        "operation_id", "resume_authority", "authorization_reason",
        "fresh_attempt_required", "human_return_point",
    }),
    PacketTemplateKind.DEPENDENCY_EVIDENCE: frozenset({
        "evidence_id", "component_name", "component_version", "source_reference",
        "source_revision", "dependency_owner", "verification_method",
    }),
    PacketTemplateKind.EXTERNAL_EVALUATION_EVIDENCE: frozenset({
        "evidence_id", "evaluation_class", "source_reference", "source_revision",
        "evidence_producer", "verification_method",
    }),
    PacketTemplateKind.HUMAN_RETURN_PACKET: frozenset({
        "operation_id", "current_state", "residual_owner", "human_return_point",
        "known_facts", "unresolved_questions", "requested_human_decision",
    }),
}

_OPTIONAL_COMMON = frozenset({"notes", "evidence_references"})
_ENVELOPE_KEYS = frozenset({"schema_version", "template_kind", "authority_effect", "payload"})


@dataclass(frozen=True)
class ResponsibilityPacket:
    schema_version: str
    template_kind: PacketTemplateKind
    payload: Mapping[str, Any]
    authority_effect: str = "none"

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "template_kind": self.template_kind.value,
            "authority_effect": self.authority_effect,
            "payload": dict(self.payload),
        }


def validate_packet(data: Mapping[str, Any]) -> ResponsibilityPacket:
    unknown_envelope = set(data) - _ENVELOPE_KEYS
    if unknown_envelope:
        raise ValueError(f"unknown packet fields: {sorted(unknown_envelope)}")
    missing_envelope = _ENVELOPE_KEYS - set(data)
    if missing_envelope:
        raise ValueError(f"missing packet fields: {sorted(missing_envelope)}")

    schema_version = data["schema_version"]
    if schema_version != "rpos.packet.v0.1":
        raise ValueError("unsupported packet schema_version")

    try:
        kind = PacketTemplateKind(str(data["template_kind"]))
    except ValueError as exc:
        raise ValueError("unsupported template_kind") from exc

    if data["authority_effect"] != "none":
        raise ValueError("packet templates cannot create authority or state transitions")

    payload = data["payload"]
    if not isinstance(payload, Mapping):
        raise ValueError("payload must be an object")

    allowed = _REQUIRED[kind] | _OPTIONAL_COMMON
    unknown_payload = set(payload) - allowed
    if unknown_payload:
        raise ValueError(f"unknown payload fields for {kind.value}: {sorted(unknown_payload)}")
    missing_payload = _REQUIRED[kind] - set(payload)
    if missing_payload:
        raise ValueError(f"missing payload fields for {kind.value}: {sorted(missing_payload)}")

    for key in _REQUIRED[kind]:
        value = payload[key]
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"required payload field must not be empty: {key}")
        if value is None:
            raise ValueError(f"required payload field must not be null: {key}")

    return ResponsibilityPacket(
        schema_version=schema_version,
        template_kind=kind,
        authority_effect="none",
        payload=dict(payload),
    )
