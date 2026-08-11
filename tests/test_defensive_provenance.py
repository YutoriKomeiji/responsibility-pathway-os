# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import pytest

from rpos import (
    DefensiveProvenanceRecord,
    DesignAroundReadiness,
    ExternalReferenceBoundary,
    ProvenanceSourceClass,
)


def _valid_payload() -> dict[str, object]:
    return {
        "record_id": "prov-001",
        "feature_id": "effect-unknown",
        "feature_name": "Effect unknown responsibility state",
        "first_known_internal_date": "2026-08-01",
        "first_known_internal_reference": "issue:153",
        "technical_rationale": "Preserve responsibility when an external effect cannot be verified.",
        "source_class": "internal_engineering",
        "source_references": ["issue:153", "spec:repair-resume"],
        "external_reference_boundary": "none",
        "design_around_readiness": "modular_boundary",
        "replaceable_boundary": "external-effect verification and reconciliation interface",
    }


def test_import_accepts_bounded_engineering_provenance() -> None:
    record = DefensiveProvenanceRecord.from_import_dict(_valid_payload())

    assert record.source_class is ProvenanceSourceClass.INTERNAL_ENGINEERING
    assert record.external_reference_boundary is ExternalReferenceBoundary.NONE
    assert record.design_around_readiness is DesignAroundReadiness.MODULAR_BOUNDARY
    assert "non_infringement" not in record.to_dict()
    assert "freedom_to_operate" not in record.to_dict()


def test_import_rejects_unknown_fields_fail_closed() -> None:
    payload = _valid_payload()
    payload["unexpected"] = "value"

    with pytest.raises(ValueError, match="unexpected fields"):
        DefensiveProvenanceRecord.from_import_dict(payload)


def test_import_rejects_legal_conclusion_fields() -> None:
    for prohibited in (
        "non_infringement",
        "invalidity",
        "freedom_to_operate",
        "prior_art_sufficient",
        "legal_conclusion",
        "claim_scope_conclusion",
    ):
        payload = _valid_payload()
        payload[prohibited] = True
        with pytest.raises(ValueError, match="prohibited legal fields"):
            DefensiveProvenanceRecord.from_import_dict(payload)


def test_modular_design_around_readiness_requires_named_boundary() -> None:
    payload = _valid_payload()
    payload.pop("replaceable_boundary")

    with pytest.raises(ValueError, match="requires replaceable_boundary"):
        DefensiveProvenanceRecord.from_import_dict(payload)


def test_public_disclosure_metadata_must_be_paired() -> None:
    payload = _valid_payload()
    payload["public_disclosure_date"] = "2026-08-09"

    with pytest.raises(ValueError, match="must be supplied together"):
        DefensiveProvenanceRecord.from_import_dict(payload)
