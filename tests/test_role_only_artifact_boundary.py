# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import ast
from pathlib import Path


RPOS_ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = RPOS_ROOT / "review"
QUICK_START = RPOS_ROOT / "examples" / "quick_start_end_to_end.py"

ALLOWED_REVIEW_HEADINGS = {
    "Integration Review",
    "Terminology Review",
    "Verification Review",
    "Human Usability Review",
    "Restart / Continuity Review",
    "Alternative Framing Review",
    "Implementation Review",
    "Provenance Review",
    "Boundary Review",
}

ALLOWED_DEMO_ROLE_VALUES = {
    "requester",
    "executor",
    "human_authority",
    "human-authority-review",
    "operator",
}

ROLE_KEYWORDS = {
    "requested_by",
    "execution_actor",
    "approval_authority",
    "human_return_point",
    "residual_owner",
    "resume_authority",
    "actor",
}


def test_review_artifacts_use_role_only_structure_when_present() -> None:
    # `review/` is a private RPP development surface and is intentionally absent
    # from the allowlisted public export. When the surface exists, validate it
    # strictly; its absence in a public export is itself an allowed boundary.
    if not REVIEW_DIR.is_dir():
        return

    review_files = sorted(REVIEW_DIR.glob("*.md"))
    assert review_files

    for path in review_files:
        assert path.name.endswith("-internal-review.md"), path.name
        text = path.read_text(encoding="utf-8")
        headings = {
            line.removeprefix("### ").strip()
            for line in text.splitlines()
            if line.startswith("### ")
        }
        assert headings
        assert headings <= ALLOWED_REVIEW_HEADINGS, (path.name, headings - ALLOWED_REVIEW_HEADINGS)


def test_quick_start_uses_generic_role_values() -> None:
    tree = ast.parse(QUICK_START.read_text(encoding="utf-8"))
    values: set[str] = set()

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg not in ROLE_KEYWORDS:
                continue
            if isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                values.add(keyword.value.value)

    assert values
    assert values <= ALLOWED_DEMO_ROLE_VALUES, values - ALLOWED_DEMO_ROLE_VALUES
