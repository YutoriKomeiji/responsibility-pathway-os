# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "provenance" / "security-quality-readiness-0.1.0a1.json"


def _load() -> dict[str, object]:
    return json.loads(READINESS.read_text(encoding="utf-8"))


def test_security_quality_readiness_record_has_required_release_identity() -> None:
    data = _load()
    assert data["schema_version"] == "rpos.security-quality-readiness.v0.1"
    assert data["release_candidate"] == "0.1.0a1"
    assert data["baseline_date"] == "2026-08-12"
    assert data["status"] == "migration_ready"


def test_security_quality_readiness_deferrals_have_responsible_return_paths() -> None:
    data = _load()
    deferrals = data["deferred_controls"]
    assert isinstance(deferrals, list)
    assert deferrals
    required = {"control", "owner", "reason", "risk", "claim_impact", "human_return_point"}
    for item in deferrals:
        assert isinstance(item, dict)
        assert required <= set(item)
        for field in required:
            assert str(item[field]).strip()


def test_security_quality_readiness_keeps_claim_ceiling_explicit() -> None:
    data = _load()
    non_claims = set(data["non_claims"])
    assert "production_readiness" in non_claims
    assert "tamper_proof_event_history" in non_claims
    assert "universal_prompt_injection_resistance" in non_claims
    assert "multi_tenant_security" in non_claims


def test_security_quality_readiness_covers_core_responsibility_security_controls() -> None:
    data = _load()
    controls = set(data["implemented_controls"])
    expected = {
        "authority_freshness_envelope",
        "responsibility_integrity_snapshot",
        "responsibility_state_non_equivocation_detection",
        "responsibility_event_chain_checkpoint",
        "evidence_supersession_chain_validation",
        "safe_responsibility_dependency_degradation",
        "external_effect_unknown_containment",
        "restart_recovery_without_redispatch",
    }
    assert expected <= controls
