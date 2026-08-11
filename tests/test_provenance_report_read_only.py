# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from rpos.provenance import DefensiveProvenanceRecord, DesignAroundReadiness, ExternalReferenceBoundary, ProvenanceSourceClass
from rpos.provenance_review import build_provenance_review_report


def test_empty_claim_review_report_is_read_only_engineering_evidence() -> None:
    feature = DefensiveProvenanceRecord(
        record_id="prov-001",
        feature_id="feature-001",
        feature_name="Example feature",
        first_known_internal_date="2026-08-08",
        technical_rationale="Example bounded engineering rationale.",
        source_class=ProvenanceSourceClass.INTERNAL_ENGINEERING,
        source_references=("issue:151",),
        external_reference_boundary=ExternalReferenceBoundary.NONE,
        design_around_readiness=DesignAroundReadiness.NOT_ASSESSED,
    )
    report = build_provenance_review_report([feature])
    assert report["claim_review_count"] == 0
    assert report["features_with_public_claim_mapping"] == []
    assert "claim_scope" in report["not_proven"]
