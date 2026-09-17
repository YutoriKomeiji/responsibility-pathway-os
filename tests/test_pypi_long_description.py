# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pypi_long_description_matches_candidate_identity() -> None:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        project = tomllib.load(fh)["project"]
    status = json.loads((ROOT / "product-status.json").read_text(encoding="utf-8"))

    readme_path = ROOT / project["readme"]
    text = readme_path.read_text(encoding="utf-8")
    version = project["version"]

    assert version in text
    assert f"responsibility-pathway-os=={version}" in text

    previous = status["latest_published_version"]
    if previous != version:
        assert f"responsibility-pathway-os=={previous}" not in text
        assert f"Version: **{previous}**" not in text


def test_pypi_long_description_is_publication_state_neutral() -> None:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        project = tomllib.load(fh)["project"]
    text = (ROOT / project["readme"]).read_text(encoding="utf-8").lower()

    forbidden = (
        "current published release",
        "currently published release",
        "release candidate / not published",
        "not yet published",
    )
    for marker in forbidden:
        assert marker not in text
