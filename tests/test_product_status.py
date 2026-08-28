# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_product_status_matches_package_identity_and_release_boundary() -> None:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        project = tomllib.load(fh)["project"]
    status = json.loads((ROOT / "product-status.json").read_text(encoding="utf-8"))

    assert status["package"] == project["name"]
    assert status["version"] == project["version"]
    assert status["release_stage"] == "early_public_alpha_publishable_freeze"
    assert status["publication_state"] == "not_published"
    assert status["production_ready"] is False
    assert status["release_gate"]["publishable_freeze"] is True
    assert status["release_gate"]["public_repository_migration_complete"] is True
    assert status["release_gate"]["pypi_trusted_publisher_configured"] is False
    assert status["release_gate"]["explicit_human_gate_required"] is True
    assert "public_product_site_deployment" in status["verified_surfaces"]


def test_product_status_keeps_high_impact_non_claims_explicit() -> None:
    status = json.loads((ROOT / "product-status.json").read_text(encoding="utf-8"))
    non_claims = set(status["explicit_non_claims"])
    assert "production_availability_or_slo" in non_claims
    assert "legal_or_compliance_certification" in non_claims
    assert "implementation_wide_formal_correctness" in non_claims
    assert "organizational_or_execution_authority" in non_claims
