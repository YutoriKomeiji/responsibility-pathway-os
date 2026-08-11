# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

from pathlib import Path

import pytest

from rpos.hash_bundle import create_hash_bundle, sha256_file
from rpos.sbom import generate_cyclonedx_sbom


ROOT = Path(__file__).resolve().parents[1]


def test_sbom_identifies_rpos_candidate_and_source_commit() -> None:
    result = generate_cyclonedx_sbom(ROOT / "pyproject.toml", source_commit="abc123")
    assert result["bomFormat"] == "CycloneDX"
    assert result["specVersion"] == "1.6"
    component = result["metadata"]["component"]
    assert component["name"] == "responsibility-pathway-os"
    assert component["version"] == "0.1.0a1"
    assert {item["name"]: item["value"] for item in component["properties"]}["rpos:source-commit"] == "abc123"


def test_sbom_requires_project_identity(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[project]\nname='x'\n", encoding="utf-8")
    with pytest.raises(ValueError):
        generate_cyclonedx_sbom(pyproject)


def test_hash_bundle_is_source_bound_and_uses_sha256(tmp_path: Path) -> None:
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_text("alpha", encoding="utf-8")
    second.write_text("beta", encoding="utf-8")
    bundle = create_hash_bundle([second, first], source_commit="deadbeef")
    assert bundle["source_commit"] == "deadbeef"
    assert [item["name"] for item in bundle["artifacts"]] == ["first.txt", "second.txt"]
    hashes = {item["name"]: item["sha256"] for item in bundle["artifacts"]}
    assert hashes["first.txt"] == sha256_file(first)
    assert len(bundle["bundle_sha256"]) == 64


def test_hash_bundle_fails_closed_for_missing_artifact(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        create_hash_bundle([tmp_path / "missing.whl"], source_commit="deadbeef")
