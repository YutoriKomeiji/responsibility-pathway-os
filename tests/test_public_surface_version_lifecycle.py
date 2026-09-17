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
        candidate = tomllib.load(fh)["project"]["version"]
    status = json.loads(_text("product-status.json"))
    assert status["version"] == candidate
    return candidate, status["latest_published_version"], status["publication_state"]


def test_unpublished_candidate_keeps_current_reader_surfaces_on_latest_published_version() -> None:
    candidate, published, publication_state = _release_state()
    assert publication_state == "not_published"
    assert candidate != published

    exact_markers = {
        "README.md": (
            f"RPOS-DOC-VERSION: {published}",
            f"Version: **{published}",
            f"responsibility-pathway-os=={published}",
        ),
        "README.ja.md": (
            f"RPOS-DOC-VERSION: {published}",
            f"Version: **{published}",
            f"responsibility-pathway-os=={published}",
        ),
        "site/index.html": (
            f"{published} Published Public Alpha",
            f"responsibility-pathway-os=={published}",
            f"/responsibility-pathway-os/{published}/",
        ),
        "site/ja.html": (
            f"{published} Published Public Alpha",
            f"responsibility-pathway-os=={published}",
            f"/responsibility-pathway-os/{published}/",
        ),
        "docs/en/current-scope-and-extension-surface.md": (
            f"RPOS-DOC-VERSION: {published}",
            f"RPOS {published}",
        ),
        "docs/ja/current-scope-and-extension-surface.md": (
            f"RPOS-DOC-VERSION: {published}",
            f"RPOS {published}",
        ),
        "docs/en/claim-boundary-promotion.md": (f"RPOS {published}",),
        "docs/ja/claim-boundary-promotion.md": (f"RPOS {published}",),
        "docs/en/responsibility-routing-current-source.md": (f"published `{published}`",),
        "docs/ja/responsibility-routing-current-source.md": (f"公開済み`{published}`",),
        "examples/production_grade_demos/README.md": (f"published RPOS `{published}` release line",),
    }

    for path, markers in exact_markers.items():
        text = _text(path)
        missing = [marker for marker in markers if marker not in text]
        assert not missing, f"{path} missing current-published markers: {missing}"


def test_unpublished_candidate_package_description_is_candidate_specific_and_publication_neutral() -> None:
    candidate, published, publication_state = _release_state()
    assert publication_state == "not_published"

    text = _text("PYPI_README.md")
    assert f"Version: **{candidate}**" in text
    assert f"responsibility-pathway-os=={candidate}" in text
    assert f"responsibility-pathway-os=={published}" not in text

    forbidden_publication_claims = (
        "current published release",
        "currently published",
        f"{candidate} is published",
        f"{candidate} has been published",
    )
    lowered = text.lower()
    for phrase in forbidden_publication_claims:
        assert phrase.lower() not in lowered


def test_active_current_surfaces_do_not_reintroduce_a2_as_current_or_install_target() -> None:
    _, published, _ = _release_state()
    assert published != "0.1.0a2"

    active_paths = (
        "README.md",
        "README.ja.md",
        "site/index.html",
        "site/ja.html",
        "docs/en/current-scope-and-extension-surface.md",
        "docs/ja/current-scope-and-extension-surface.md",
        "docs/en/claim-boundary-promotion.md",
        "docs/ja/claim-boundary-promotion.md",
        "docs/en/responsibility-routing-current-source.md",
        "docs/ja/responsibility-routing-current-source.md",
        "examples/production_grade_demos/README.md",
    )

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
    # Historical evidence may and should retain older version identities.
    history = _text("release-history/0.1.0a3-candidate.md")
    assert "0.1.0a2" in history
