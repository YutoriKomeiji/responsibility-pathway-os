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


def _identity_markers(version: str) -> dict[str, tuple[str, ...]]:
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
        "site/index.html": (version, f"responsibility-pathway-os=={version}"),
        "site/ja.html": (version, f"responsibility-pathway-os=={version}"),
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
        "docs/en/public-alpha-evaluation-guide.md": (
            f"RPOS {version}",
            f"responsibility-pathway-os=={version}",
        ),
        "docs/ja/public-alpha-evaluation-guide.md": (
            f"RPOS {version}",
            f"responsibility-pathway-os=={version}",
        ),
        "docs/en/responsibility-routing-current-source.md": (version,),
        "docs/ja/responsibility-routing-current-source.md": (version,),
        "examples/production_grade_demos/README.md": (version,),
        "PYPI_README.md": (f"Version: **{version}**", f"responsibility-pathway-os=={version}"),
        "formal/assurance-catalog.json": (f'"product_version": "{version}"',),
    }


def test_active_release_identity_is_future_version_first() -> None:
    version, published, publication_state = _release_state()

    # Active/current-facing sources always carry the release being prepared,
    # even before that release has been published externally.
    for path, markers in _identity_markers(version).items():
        text = _text(path)
        missing = [marker for marker in markers if marker not in text]
        assert not missing, f"{path} missing active release identity markers: {missing}"

    if publication_state == "not_published":
        assert version != published
        for path in ("README.md", "README.ja.md", "site/index.html", "site/ja.html"):
            lowered = _text(path).lower()
            assert "candidate" in lowered or "not yet published" in lowered or "未公開" in lowered
    else:
        assert publication_state == "pypi_published"
        assert version == published


def test_formal_assurance_product_version_matches_package_version() -> None:
    version, _, _ = _release_state()
    catalog = json.loads(_text("formal/assurance-catalog.json"))
    assert catalog["product_version"] == version


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


def test_active_surfaces_do_not_reintroduce_a2_as_current_or_install_target() -> None:
    active_paths = tuple(_identity_markers(_release_state()[0]))
    stale_patterns = (
        re.compile(r"responsibility-pathway-os==0\.1\.0a2"),
        re.compile(r"0\.1\.0a2 Published Public Alpha"),
        re.compile(r"RPOS-DOC-VERSION: 0\.1\.0a2"),
        re.compile(r'"product_version"\s*:\s*"0\.1\.0a2"'),
    )

    for path in active_paths:
        text = _text(path)
        hits = [pattern.pattern for pattern in stale_patterns if pattern.search(text)]
        assert not hits, f"{path} reintroduces stale a2 current/install semantics: {hits}"


def test_historical_release_records_are_not_forced_to_current_version() -> None:
    history = _text("release-history/0.1.0a3-candidate.md")
    assert "0.1.0a2" in history
