# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import re
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _project_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        return tomllib.load(fh)["project"]["version"]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_public_readmes_match_project_version() -> None:
    version = _project_version()
    for path in ("README.md", "README.ja.md"):
        text = _read(path)
        assert f"RPOS-DOC-VERSION: {version}" in text
        assert f"Version: **{version} candidate" in text
        assert f"responsibility-pathway-os=={version}" in text


def test_release_provenance_filenames_match_project_version() -> None:
    version = _project_version()
    expected = {
        f"migration-provenance-snapshot-{version}.json",
        f"security-quality-readiness-{version}.json",
    }
    actual = {path.name for path in (ROOT / "provenance").glob("*0.1.0a*.json")}
    assert expected <= actual


def test_project_metadata_has_release_identity() -> None:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        project = tomllib.load(fh)["project"]
    assert project["name"] == "responsibility-pathway-os"
    assert project["license"] == "MIT"
    assert project["requires-python"].startswith(">=3.11")
    assert project["scripts"]["rpos"] == "rpos.cli:main"
    assert re.fullmatch(r"0\.1\.0a\d+", project["version"])
