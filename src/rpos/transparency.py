# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class TransparencyDutyClass(StrEnum):
    AI_INTERACTION = "ai_interaction"
    SYNTHETIC_CONTENT = "synthetic_content"
    DEPLOYER_DISCLOSURE = "deployer_disclosure"
    HUMAN_EDITORIAL_REVIEW = "human_editorial_review"


class TransparencyStatus(StrEnum):
    NOT_APPLICABLE_BY_CONFIG = "not_applicable_by_config"
    REQUIRED_PENDING = "required_pending"
    PRESENTED_UNVERIFIED = "presented_unverified"
    VERIFIED = "verified"
    GAP_REQUIRES_REVIEW = "gap_requires_review"


@dataclass(frozen=True)
class TransparencyEnvelope:
    operation_id: str
    provider_or_deployer_role: str
    transparency_duty_class: TransparencyDutyClass
    content_or_interaction_id: str
    responsible_actor: str
    status: TransparencyStatus
    evidence_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "operation_id",
            "provider_or_deployer_role",
            "content_or_interaction_id",
            "responsible_actor",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["transparency_duty_class"] = self.transparency_duty_class.value
        value["status"] = self.status.value
        return value


@dataclass(frozen=True)
class AIInteractionDisclosure:
    envelope: TransparencyEnvelope
    disclosure_text: str
    disclosure_surface: str
    locale: str | None = None
    accessibility_note: str | None = None
    presented: bool = False
    presentation_evidence_ref: str | None = None

    def __post_init__(self) -> None:
        if self.envelope.transparency_duty_class is not TransparencyDutyClass.AI_INTERACTION:
            raise ValueError("envelope duty class must be ai_interaction")
        if not self.disclosure_text.strip():
            raise ValueError("disclosure_text must not be empty")
        if not self.disclosure_surface.strip():
            raise ValueError("disclosure_surface must not be empty")
        if self.presentation_evidence_ref and not self.presented:
            raise ValueError("presentation evidence requires presented=True")


@dataclass(frozen=True)
class SyntheticContentProvenance:
    envelope: TransparencyEnvelope
    content_hash: str
    generation_class: str
    marker_profile: str | None
    marker_inserted: bool
    marker_verified: bool | None
    marker_evidence_ref: str | None = None

    def __post_init__(self) -> None:
        if self.envelope.transparency_duty_class is not TransparencyDutyClass.SYNTHETIC_CONTENT:
            raise ValueError("envelope duty class must be synthetic_content")
        if not self.content_hash.strip():
            raise ValueError("content_hash must not be empty")
        if not self.generation_class.strip():
            raise ValueError("generation_class must not be empty")
        if self.marker_verified is True and not self.marker_inserted:
            raise ValueError("marker cannot be verified when it was not inserted")
        if self.marker_evidence_ref and self.marker_verified is not True:
            raise ValueError("marker evidence requires marker_verified=True")


@dataclass(frozen=True)
class HumanEditorialResponsibility:
    envelope: TransparencyEnvelope
    reviewed: bool
    reviewer: str | None = None
    editorial_control_summary: str | None = None

    def __post_init__(self) -> None:
        if self.envelope.transparency_duty_class is not TransparencyDutyClass.HUMAN_EDITORIAL_REVIEW:
            raise ValueError("envelope duty class must be human_editorial_review")
        if self.reviewed and (self.reviewer is None or not self.reviewer.strip()):
            raise ValueError("reviewer is required when reviewed=True")


def disclosure_grants_authority(_: AIInteractionDisclosure) -> bool:
    """Transparency evidence never grants operational authority."""
    return False


def marker_proves_content_truth(_: SyntheticContentProvenance) -> bool:
    """Origin/marking evidence is not factual-truth evidence."""
    return False


def human_review_proves_legal_compliance(_: HumanEditorialResponsibility) -> bool:
    """Human review evidence is not a legal-compliance determination."""
    return False
