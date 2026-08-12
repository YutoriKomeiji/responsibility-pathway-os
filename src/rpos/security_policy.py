# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable, Mapping

from .security import SecurityDisposition


@dataclass(frozen=True)
class EvidenceSupersessionRecord:
    """One immutable link in an evidence supersession chain.

    A newer record may supersede an earlier evidence item, but the earlier identity
    and digest remain part of the chain. This models anti-substitution provenance;
    it does not prove that evidence content is true.
    """

    evidence_id: str
    evidence_digest: str
    source_reference: str
    supersedes_id: str | None = None
    reason: str | None = None

    def __post_init__(self) -> None:
        for name in ("evidence_id", "evidence_digest", "source_reference"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must not be empty")
        if self.supersedes_id is not None and not self.supersedes_id.strip():
            raise ValueError("supersedes_id must not be empty when supplied")
        if self.reason is not None and not self.reason.strip():
            raise ValueError("reason must not be empty when supplied")
        if self.supersedes_id == self.evidence_id:
            raise ValueError("evidence cannot supersede itself")


@dataclass(frozen=True)
class EvidenceChainValidation:
    valid: bool
    reasons: tuple[str, ...]
    head_evidence_id: str | None


def validate_evidence_supersession_chain(
    records: Iterable[EvidenceSupersessionRecord],
) -> EvidenceChainValidation:
    """Validate one ordered evidence lineage without erasing prior evidence.

    The first record is the retained root. Every later record must explicitly point
    to the immediately previous evidence id. Duplicate ids, missing predecessor
    links, cycles, and silent replacements are rejected.
    """

    sequence = tuple(records)
    if not sequence:
        return EvidenceChainValidation(valid=True, reasons=(), head_evidence_id=None)

    reasons: list[str] = []
    seen: set[str] = set()
    previous_id: str | None = None
    for index, record in enumerate(sequence):
        if record.evidence_id in seen:
            reasons.append(f"duplicate_evidence_id:{record.evidence_id}")
        if index == 0:
            if record.supersedes_id is not None:
                reasons.append("root_must_not_supersede_unknown_predecessor")
        else:
            if record.supersedes_id is None:
                reasons.append(f"silent_replacement_without_supersession:{record.evidence_id}")
            elif record.supersedes_id != previous_id:
                reasons.append(
                    f"broken_supersession_link:{record.evidence_id}:expected:{previous_id}:actual:{record.supersedes_id}"
                )
            if record.supersedes_id in seen and record.supersedes_id != previous_id:
                reasons.append(f"supersession_cycle_or_branch:{record.evidence_id}")
        seen.add(record.evidence_id)
        previous_id = record.evidence_id

    return EvidenceChainValidation(
        valid=not reasons,
        reasons=tuple(reasons),
        head_evidence_id=sequence[-1].evidence_id,
    )


class ResponsibilityDependencyCriticality(StrEnum):
    AUTHORITY = "authority"
    IDENTITY = "identity"
    POLICY = "policy"
    EFFECT_VERIFICATION = "effect_verification"
    SUPPORTING = "supporting"


class ResponsibilityDependencyHealth(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class ResponsibilityDependencyStatus:
    name: str
    criticality: ResponsibilityDependencyCriticality
    health: ResponsibilityDependencyHealth

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("dependency name must not be empty")


@dataclass(frozen=True)
class ResponsibilityDegradationDecision:
    disposition: SecurityDisposition
    reasons: tuple[str, ...]
    degraded_dependencies: tuple[str, ...]

    @property
    def allowed(self) -> bool:
        return self.disposition is SecurityDisposition.ALLOW


def evaluate_responsibility_degradation(
    statuses: Iterable[ResponsibilityDependencyStatus],
) -> ResponsibilityDegradationDecision:
    """Fail closed for unavailable responsibility-critical dependencies.

    Supporting dependencies may degrade or become unavailable without granting new
    authority. Such degradation remains explicit in the returned decision so it can
    be surfaced to operators and telemetry.
    """

    sequence = tuple(statuses)
    names: set[str] = set()
    reasons: list[str] = []
    degraded: list[str] = []
    hold = False

    for status in sequence:
        if status.name in names:
            raise ValueError(f"duplicate dependency status: {status.name}")
        names.add(status.name)
        if status.health is ResponsibilityDependencyHealth.AVAILABLE:
            continue
        degraded.append(status.name)
        if status.criticality is ResponsibilityDependencyCriticality.SUPPORTING:
            reasons.append(f"supporting_dependency_{status.health.value}:{status.name}")
            continue
        hold = True
        reasons.append(
            f"critical_dependency_{status.health.value}:{status.criticality.value}:{status.name}"
        )

    return ResponsibilityDegradationDecision(
        disposition=SecurityDisposition.HOLD if hold else SecurityDisposition.ALLOW,
        reasons=tuple(reasons),
        degraded_dependencies=tuple(degraded),
    )


def evaluate_named_responsibility_dependencies(
    statuses: Mapping[str, tuple[ResponsibilityDependencyCriticality, ResponsibilityDependencyHealth]],
) -> ResponsibilityDegradationDecision:
    """Convenience wrapper for configuration-driven dependency status maps."""

    return evaluate_responsibility_degradation(
        ResponsibilityDependencyStatus(name=name, criticality=criticality, health=health)
        for name, (criticality, health) in statuses.items()
    )
