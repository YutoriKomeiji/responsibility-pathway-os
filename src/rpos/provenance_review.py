# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from .provenance import DefensiveProvenanceRecord


class ClaimReviewStatus(StrEnum):
    NOT_STARTED = "not_started"
    PUBLIC_CLAIM_AVAILABLE = "public_claim_available"
    QUALIFIED_REVIEW_REQUIRED = "qualified_review_required"
    DESIGN_AROUND_REVIEW = "design_around_review"
    CLOSED_NO_ENGINEERING_CHANGE = "closed_no_engineering_change"
    CLOSED_ENGINEERING_CHANGE = "closed_engineering_change"


_REQUIRED_CLAIM_FIELDS = {
    "review_id",
    "publication_number",
    "claim_identifier",
    "publication_date",
    "claim_text_reference",
    "review_status",
}
_OPTIONAL_CLAIM_FIELDS = {
    "application_number",
    "priority_date",
    "issued_patent_number",
    "issued_claim_version",
    "mapped_feature_ids",
    "engineering_notes",
}
_ALLOWED_CLAIM_FIELDS = _REQUIRED_CLAIM_FIELDS | _OPTIONAL_CLAIM_FIELDS


@dataclass(frozen=True)
class PublicClaimReviewRecord:
    review_id: str
    publication_number: str
    claim_identifier: str
    publication_date: str
    claim_text_reference: str
    review_status: ClaimReviewStatus
    application_number: str | None = None
    priority_date: str | None = None
    issued_patent_number: str | None = None
    issued_claim_version: str | None = None
    mapped_feature_ids: tuple[str, ...] = ()
    engineering_notes: str | None = None

    def __post_init__(self) -> None:
        for name in ("review_id", "publication_number", "claim_identifier", "publication_date", "claim_text_reference"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if self.issued_claim_version is not None and self.issued_patent_number is None:
            raise ValueError("issued_claim_version requires issued_patent_number")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["mapped_feature_ids"] = list(self.mapped_feature_ids)
        return value

    @classmethod
    def from_import_dict(cls, value: dict[str, Any]) -> "PublicClaimReviewRecord":
        fields = set(value)
        missing = sorted(_REQUIRED_CLAIM_FIELDS - fields)
        unexpected = sorted(fields - _ALLOWED_CLAIM_FIELDS)
        if missing:
            raise ValueError(f"claim review record is missing required fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"claim review record contains unexpected fields: {', '.join(unexpected)}")
        mapped = value.get("mapped_feature_ids", [])
        if not isinstance(mapped, list):
            raise ValueError("mapped_feature_ids must be a JSON array")
        def optional(name: str) -> str | None:
            item = value.get(name)
            return None if item is None else str(item)
        return cls(
            review_id=str(value["review_id"]),
            publication_number=str(value["publication_number"]),
            claim_identifier=str(value["claim_identifier"]),
            publication_date=str(value["publication_date"]),
            claim_text_reference=str(value["claim_text_reference"]),
            review_status=ClaimReviewStatus(str(value["review_status"])),
            application_number=optional("application_number"),
            priority_date=optional("priority_date"),
            issued_patent_number=optional("issued_patent_number"),
            issued_claim_version=optional("issued_claim_version"),
            mapped_feature_ids=tuple(str(item) for item in mapped),
            engineering_notes=optional("engineering_notes"),
        )


def build_provenance_review_report(
    provenance_records: list[DefensiveProvenanceRecord],
    claim_reviews: list[PublicClaimReviewRecord] | None = None,
) -> dict[str, Any]:
    claims = claim_reviews or []
    mapped = {feature_id for claim in claims for feature_id in claim.mapped_feature_ids}
    return {
        "schema_version": "rpos.provenance-review.v0.1",
        "feature_count": len(provenance_records),
        "claim_review_count": len(claims),
        "features": [record.to_dict() for record in provenance_records],
        "claim_reviews": [record.to_dict() for record in claims],
        "features_with_public_claim_mapping": sorted(mapped),
        "not_proven": [
            "patent_non_infringement",
            "patent_invalidity",
            "freedom_to_operate",
            "prior_art_sufficiency",
            "claim_scope",
            "legal_advice",
        ],
    }
