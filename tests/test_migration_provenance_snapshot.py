# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import json
from pathlib import Path


SNAPSHOT = Path(__file__).resolve().parents[1] / "provenance" / "migration-provenance-snapshot-0.1.0a1.json"


def _load() -> dict[str, object]:
    return json.loads(SNAPSHOT.read_text(encoding="utf-8"))


def test_snapshot_preserves_private_to_public_transition_boundary() -> None:
    data = _load()
    repo = data["standalone_repository"]
    assert repo["created_private"] is True
    assert repo["public_transition_at_utc"] is None
    assert repo["public_transition_authorized"] is False


def test_snapshot_is_not_a_false_final_freeze() -> None:
    data = _load()
    freeze = data["freeze_state"]
    assert freeze["exact_rpp_source_sha"] is None
    assert freeze["export_manifest_hash"] is None
    assert freeze["final_freeze_complete"] is False


def test_snapshot_excludes_private_comparison_material_from_export() -> None:
    data = _load()
    boundary = data["independent_design_boundary"]
    assert boundary["private_third_party_research_exported"] is False
    assert boundary["third_party_claims_used_as_normative_feature_rationale"] is False
    assert boundary["legal_conclusions_in_snapshot"] is False


def test_snapshot_keeps_non_claims_explicit() -> None:
    data = _load()
    not_proven = set(data["not_proven"])
    assert "patent non-infringement" in not_proven
    assert "freedom to operate" in not_proven
    assert "legal or regulatory compliance" in not_proven
    assert "production readiness" in not_proven


def test_snapshot_records_layered_responsibility_pathway_lineage() -> None:
    data = _load()
    layers = [item["layer"] for item in data["lineage"]]
    assert layers == ["RPD", "RPE", "RPR", "RPOS"]
