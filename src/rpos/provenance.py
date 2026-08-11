# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class ProvenanceSourceClass(StrEnum):
    INTERNAL_ENGINEERING = "internal_engineering"
    PUBLIC_STANDARD_OR_GUIDANCE = "public_standard_or_guidance"
    GENERAL_ENGINEERING = "general_engineering"
    EXTERNAL_COMPARISON = "external_comparison"
    DECLARED_DEPENDENCY = "declared_dependency"


class ExternalReferenceBoundary(StrEnum):
    NONE = "none"
    CONTEXT_ONLY = "context_only"
    COMPARISON_ONLY = "comparison_only"
    DECLARED_DEPENDENCY = "declared_dependency"


class DesignAroundReadiness(StrEnum):
    NOT_ASSESSED = "not_assessed"
    MODULAR_BOUNDARY = "modular_boundary"
    COUPLED_REVIEW_REQUIRED = "coupled_review_required"


_REQUIRED_FIELDS = {
    "record_id",
    "feature_id",
    "feature_name",
    "first_known_internal_date",
    "technical_rationale",
    "source_class",
    "source_references",
    "external_reference_boundary",
    "design_around_readiness",
}
_OPTIONAL_FIELDS = {
    "first_known_internal_reference",
    "public_disclosure_date",
    "public_disclosure_reference",
    "replaceable_boundary",
    "notes",
}
_ALLOWED_FIELDS = _REQUIRED_FIELDS | _OPTIONAL_FIELDS

_PROHIBITED_LEGAL_FIELDS = {
    "non_infringement",
    "invalidity",
    "freedom_to_operate",
    "prior_art_sufficient",
    "legal_conclusion",
    "claim_scope_conclusion",
}


@dataclass(frozen=True)
class DefensiveProvenanceRecord:
    """Engineering provenance for later qualified review, not a legal conclusion."""

    record_id: str
    feature_id: str
    feature_name: str
    first_known_internal_date: str
    technical_rationale: str
    source_class: ProvenanceSourceClass
    source_references: tuple[str, ...]
    external_reference_boundary: ExternalReferenceBoundary
    design_around_readiness: DesignAroundReadiness
    first_known_internal_reference: str | None = None
    public_disclosure_date: str | None = None
    public_disclosure_reference: str | None = None
    replaceable_boundary: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "record_id",
            "feature_id",
            "feature_name",
            "first_known_internal_date",
            "technical_rationale",
        ):
            value = getattr(self, name)
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        if not self.source_references:
            raise ValueError("source_references must not be empty")
        if any(not item.strip() for item in self.source_references):
            raise ValueError("source_references must not contain empty values")
        for name in (
            "first_known_internal_reference",
            "public_disclosure_date",
            "public_disclosure_reference",
            "replaceable_boundary",
            "notes",
        ):
            value = getattr(self, name)
            if value is not None and not value.strip():
                raise ValueError(f"{name} must not be empty when supplied")
        if (self.public_disclosure_date is None) != (self.public_disclosure_reference is None):
            raise ValueError("public disclosure date and reference must be supplied together")
        if self.design_around_readiness is DesignAroundReadiness.MODULAR_BOUNDARY and self.replaceable_boundary is None:
            raise ValueError("modular_boundary readiness requires replaceable_boundary")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["source_references"] = list(self.source_references)
        return value

    @classmethod
    def from_import_dict(cls, value: dict[str, Any]) -> "DefensiveProvenanceRecord":
        fields = set(value)
        prohibited = sorted(fields & _PROHIBITED_LEGAL_FIELDS)
        missing = sorted(_REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - _ALLOWED_FIELDS)
        if prohibited:
            raise ValueError(f"provenance record contains prohibited legal fields: {', '.join(prohibited)}")
        if missing:
            raise ValueError(f"provenance record is missing required fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"provenance record contains unexpected fields: {', '.join(unexpected)}")

        refs = value["source_references"]
        if not isinstance(refs, list):
            raise ValueError("source_references must be a JSON array")

        def optional_text(name: str) -> str | None:
            item = value.get(name)
            return None if item is None else str(item)

        return cls(
            record_id=str(value["record_id"]),
            feature_id=str(value["feature_id"]),
            feature_name=str(value["feature_name"]),
            first_known_internal_date=str(value["first_known_internal_date"]),
            technical_rationale=str(value["technical_rationale"]),
            source_class=ProvenanceSourceClass(str(value["source_class"])),
            source_references=tuple(str(item) for item in refs),
            external_reference_boundary=ExternalReferenceBoundary(str(value["external_reference_boundary"])),
            design_around_readiness=DesignAroundReadiness(str(value["design_around_readiness"])),
            first_known_internal_reference=optional_text("first_known_internal_reference"),
            public_disclosure_date=optional_text("public_disclosure_date"),
            public_disclosure_reference=optional_text("public_disclosure_reference"),
            replaceable_boundary=optional_text("replaceable_boundary"),
            notes=optional_text("notes"),
        )
