# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from rpos.provenance import (
    DefensiveProvenanceRecord,
    DesignAroundReadiness,
    ExternalReferenceBoundary,
    ProvenanceSourceClass,
)
from rpos.provenance_review import ClaimReviewStatus, PublicClaimReviewRecord, build_provenance_review_report


def _feature() -> DefensiveProvenanceRecord:
    return DefensiveProvenanceRecord(
        record_id="prov-001",
        feature_id="RPOS-FEATURE-EFFECT-UNKNOWN",
        feature_name="Uncertain external-effect state",
        first_known_internal_date="2026-08-01",
        technical_rationale="Preserve responsibility when dispatch receipt does not prove external effect.",
        source_class=ProvenanceSourceClass.INTERNAL_ENGINEERING,
        source_references=("issue:151", "spec:rpos-state-model"),
        external_reference_boundary=ExternalReferenceBoundary.NONE,
        design_around_readiness=DesignAroundReadiness.MODULAR_BOUNDARY,
        replaceable_boundary="effect observer and reconciliation adapter",
    )


def test_claim_review_requires_actual_publication_metadata() -> None:
    record = PublicClaimReviewRecord.from_import_dict(
        {
            "review_id": "claim-review-001",
            "publication_number": "JP-EXAMPLE",
            "claim_identifier": "claim-1",
            "publication_date": "2027-01-01",
            "claim_text_reference": "official-publication:claim-1",
            "review_status": "public_claim_available",
            "priority_date": "2025-01-01",
            "mapped_feature_ids": ["RPOS-FEATURE-EFFECT-UNKNOWN"],
        }
    )
    assert record.review_status is ClaimReviewStatus.PUBLIC_CLAIM_AVAILABLE
    assert record.priority_date == "2025-01-01"


def test_claim_review_fails_closed_on_unexpected_legal_conclusion() -> None:
    payload = {
        "review_id": "claim-review-001",
        "publication_number": "JP-EXAMPLE",
        "claim_identifier": "claim-1",
        "publication_date": "2027-01-01",
        "claim_text_reference": "official-publication:claim-1",
        "review_status": "public_claim_available",
        "non_infringement": True,
    }
    try:
        PublicClaimReviewRecord.from_import_dict(payload)
    except ValueError as exc:
        assert "unexpected fields" in str(exc)
    else:
        raise AssertionError("unexpected legal-conclusion field must be rejected")


def test_provenance_report_keeps_legal_conclusions_not_proven() -> None:
    claim = PublicClaimReviewRecord(
        review_id="claim-review-001",
        publication_number="JP-EXAMPLE",
        claim_identifier="claim-1",
        publication_date="2027-01-01",
        claim_text_reference="official-publication:claim-1",
        review_status=ClaimReviewStatus.QUALIFIED_REVIEW_REQUIRED,
        mapped_feature_ids=("RPOS-FEATURE-EFFECT-UNKNOWN",),
    )
    report = build_provenance_review_report([_feature()], [claim])
    assert report["features_with_public_claim_mapping"] == ["RPOS-FEATURE-EFFECT-UNKNOWN"]
    assert "patent_non_infringement" in report["not_proven"]
    assert "freedom_to_operate" in report["not_proven"]
