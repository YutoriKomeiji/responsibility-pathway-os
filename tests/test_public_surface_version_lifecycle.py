# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _release_state() -> tuple[str, str, str]:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        version = tomllib.load(fh)["project"]["version"]
    status = json.loads(_text("product-status.json"))
    assert status["version"] == version
    return version, status["latest_published_version"], status["publication_state"]


def _current_markers(version: str) -> dict[str, tuple[str, ...]]:
    return {
        "README.md": (
            f"RPOS-DOC-VERSION: {version}",
            f"Version: **{version}",
            f"responsibility-pathway-os=={version}",
        ),
        "README.ja.md": (
            f"RPOS-DOC-VERSION: {version}",
            f"Version: **{version}",
            f"responsibility-pathway-os=={version}",
        ),
        "site/index.html": (
            f"{version} Published Public Alpha",
            f"responsibility-pathway-os=={version}",
            f"/responsibility-pathway-os/{version}/",
        ),
        "site/ja.html": (
            f"{version} Published Public Alpha",
            f"responsibility-pathway-os=={version}",
            f"/responsibility-pathway-os/{version}/",
        ),
        "docs/en/current-scope-and-extension-surface.md": (
            f"RPOS-DOC-VERSION: {version}",
            f"RPOS {version}",
        ),
        "docs/ja/current-scope-and-extension-surface.md": (
            f"RPOS-DOC-VERSION: {version}",
            f"RPOS {version}",
        ),
        "docs/en/claim-boundary-promotion.md": (f"RPOS {version}",),
        "docs/ja/claim-boundary-promotion.md": (f"RPOS {version}",),
        "docs/en/responsibility-routing-current-source.md": (f"published `{version}`",),
        "docs/ja/responsibility-routing-current-source.md": (f"公開済み`{version}`",),
        "examples/production_grade_demos/README.md": (f"published RPOS `{version}` release line",),
    }


def test_current_reader_surfaces_match_release_lifecycle_state() -> None:
    version, published, publication_state = _release_state()
    if publication_state == "not_published":
        assert version != published
        current = published
    else:
        assert publication_state == "pypi_published"
        assert version == published
        current = version

    for path, markers in _current_markers(current).items():
        text = _text(path)
        missing = [marker for marker in markers if marker not in text]
        assert not missing, f"{path} missing current-published markers: {missing}"


def test_package_description_is_version_specific_and_publication_neutral() -> None:
    version, published, _ = _release_state()
    text = _text("PYPI_README.md")
    assert f"Version: **{version}**" in text
    assert f"responsibility-pathway-os=={version}" in text
    if published != version:
        assert f"responsibility-pathway-os=={published}" not in text

    forbidden_publication_claims = (
        "current published release",
        "currently published",
        f"{version} is published",
        f"{version} has been published",
    )
    lowered = text.lower()
    for phrase in forbidden_publication_claims:
        assert phrase.lower() not in lowered


def test_active_current_surfaces_do_not_reintroduce_a2_as_current_or_install_target() -> None:
    _, published, _ = _release_state()
    assert published != "0.1.0a2"

    active_paths = tuple(_current_markers(published))
    stale_patterns = (
        re.compile(r"responsibility-pathway-os==0\.1\.0a2"),
        re.compile(r"0\.1\.0a2 Published Public Alpha"),
        re.compile(r"RPOS-DOC-VERSION: 0\.1\.0a2"),
        re.compile(r"RPOS 0\.1\.0a2 (?:is|は).*(?:published|公開済み)"),
    )

    for path in active_paths:
        text = _text(path)
        hits = [pattern.pattern for pattern in stale_patterns if pattern.search(text)]
        assert not hits, f"{path} reintroduces stale a2 current/install semantics: {hits}"


def test_historical_release_records_are_not_forced_to_current_version() -> None:
    history = _text("release-history/0.1.0a3-candidate.md")
    assert "0.1.0a2" in history
