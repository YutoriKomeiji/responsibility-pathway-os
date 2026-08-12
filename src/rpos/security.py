# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Iterable, Mapping


class SecurityDisposition(StrEnum):
    ALLOW = "allow"
    HOLD = "hold"


@dataclass(frozen=True)
class AuthorityEnvelope:
    """Context- and time-bound authority evidence for one operation/action.

    This is an additive security primitive. Existing RPOS authorization state remains
    authoritative unless a caller explicitly adopts envelope validation.
    """

    actor: str
    operation_id: str
    action_name: str
    issued_at: datetime
    expires_at: datetime
    evidence_digest: str
    context_digest: str

    def __post_init__(self) -> None:
        for field_name in ("actor", "operation_id", "action_name", "evidence_digest", "context_digest"):
            if not str(getattr(self, field_name)).strip():
                raise ValueError(f"{field_name} must not be empty")
        if self.issued_at.tzinfo is None or self.expires_at.tzinfo is None:
            raise ValueError("authority envelope timestamps must be timezone-aware")
        if self.expires_at <= self.issued_at:
            raise ValueError("expires_at must be later than issued_at")


@dataclass(frozen=True)
class AuthorityValidation:
    disposition: SecurityDisposition
    reasons: tuple[str, ...]

    @property
    def allowed(self) -> bool:
        return self.disposition is SecurityDisposition.ALLOW


def validate_authority_envelope(
    envelope: AuthorityEnvelope,
    *,
    now: datetime,
    expected_actor: str,
    expected_operation_id: str,
    expected_action_name: str,
    expected_evidence_digest: str,
    expected_context_digest: str,
) -> AuthorityValidation:
    """Fail closed when authority is stale, replayed, or detached from context."""

    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    reasons: list[str] = []
    if now < envelope.issued_at:
        reasons.append("authority_not_yet_valid")
    if now >= envelope.expires_at:
        reasons.append("authority_expired")
    if envelope.actor != expected_actor:
        reasons.append("authority_actor_mismatch")
    if envelope.operation_id != expected_operation_id:
        reasons.append("authority_operation_mismatch")
    if envelope.action_name != expected_action_name:
        reasons.append("authority_action_mismatch")
    if envelope.evidence_digest != expected_evidence_digest:
        reasons.append("authority_evidence_mismatch")
    if envelope.context_digest != expected_context_digest:
        reasons.append("authority_context_mismatch")
    disposition = SecurityDisposition.HOLD if reasons else SecurityDisposition.ALLOW
    return AuthorityValidation(disposition=disposition, reasons=tuple(reasons))


@dataclass(frozen=True)
class ResponsibilityIntegritySnapshot:
    """Canonical integrity projection of responsibility-critical state."""

    operation_id: str
    state: str
    residual_owner: str
    human_return_point: str
    event_count: int
    latest_event_digest: str

    def __post_init__(self) -> None:
        for field_name in ("operation_id", "state", "residual_owner", "human_return_point", "latest_event_digest"):
            if not str(getattr(self, field_name)).strip():
                raise ValueError(f"{field_name} must not be empty")
        if self.event_count < 0:
            raise ValueError("event_count must not be negative")

    def canonical_digest(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class ResponsibilityEventChainCheckpoint:
    """Tamper-sensitive checkpoint for the complete observed event history.

    The checkpoint is useful only when the expected digest is retained independently
    from the mutable event store. It is not a signature or trusted timestamp.
    """

    operation_id: str
    event_count: int
    chain_digest: str

    def __post_init__(self) -> None:
        if not self.operation_id.strip():
            raise ValueError("operation_id must not be empty")
        if self.event_count < 0:
            raise ValueError("event_count must not be negative")
        if not self.chain_digest.strip():
            raise ValueError("chain_digest must not be empty")


def _canonical_json_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_event_chain_checkpoint(
    operation_id: str,
    events: Iterable[Mapping[str, Any]],
) -> ResponsibilityEventChainCheckpoint:
    """Hash-chain the complete observed responsibility event sequence."""

    if not operation_id.strip():
        raise ValueError("operation_id must not be empty")
    chain = hashlib.sha256(b"rpos-responsibility-event-chain-v1").hexdigest()
    count = 0
    previous_seq: int | None = None
    for event in events:
        event_operation = str(event.get("operation_id", ""))
        if event_operation != operation_id:
            raise ValueError("event operation_id does not match checkpoint operation")
        seq = int(event["seq"])
        if previous_seq is not None and seq <= previous_seq:
            raise ValueError("events must be strictly ordered by seq")
        event_digest = _canonical_json_digest(event)
        chain = hashlib.sha256(f"{chain}:{event_digest}".encode("utf-8")).hexdigest()
        count += 1
        previous_seq = seq
    return ResponsibilityEventChainCheckpoint(operation_id=operation_id, event_count=count, chain_digest=chain)


def event_chain_matches(
    expected: ResponsibilityEventChainCheckpoint,
    events: Iterable[Mapping[str, Any]],
) -> bool:
    actual = build_event_chain_checkpoint(expected.operation_id, events)
    return actual == expected


@dataclass(frozen=True)
class ResponsibilityConsistencyFinding:
    operation_id: str
    code: str
    details: str


def find_responsibility_inconsistencies(
    snapshots: Iterable[ResponsibilityIntegritySnapshot],
) -> tuple[ResponsibilityConsistencyFinding, ...]:
    """Detect non-equivocation violations across multiple responsibility views.

    The function does not choose a winner. Any disagreement is returned for HOLD /
    responsible review by the caller.
    """

    grouped: dict[str, list[ResponsibilityIntegritySnapshot]] = {}
    for snapshot in snapshots:
        grouped.setdefault(snapshot.operation_id, []).append(snapshot)

    findings: list[ResponsibilityConsistencyFinding] = []
    for operation_id, group in grouped.items():
        if len(group) < 2:
            continue
        fields = (
            ("state", "responsibility_state_conflict"),
            ("residual_owner", "residual_owner_conflict"),
            ("human_return_point", "human_return_point_conflict"),
        )
        for field_name, code in fields:
            values = {getattr(item, field_name) for item in group}
            if len(values) > 1:
                findings.append(
                    ResponsibilityConsistencyFinding(
                        operation_id=operation_id,
                        code=code,
                        details=f"conflicting {field_name}: {sorted(values)}",
                    )
                )
        event_counts = {item.event_count for item in group}
        if len(event_counts) > 1:
            findings.append(
                ResponsibilityConsistencyFinding(
                    operation_id=operation_id,
                    code="event_history_length_conflict",
                    details=f"conflicting event_count: {sorted(event_counts)}",
                )
            )
        latest_digests = {item.latest_event_digest for item in group}
        if len(latest_digests) > 1:
            findings.append(
                ResponsibilityConsistencyFinding(
                    operation_id=operation_id,
                    code="latest_event_digest_conflict",
                    details="latest event digests disagree across responsibility views",
                )
            )
    return tuple(findings)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
