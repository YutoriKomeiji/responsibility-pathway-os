# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

from tools.build_public_export_manifest import build_manifest


def test_exact_head_public_export_is_deterministic_and_source_bound() -> None:
    first = build_manifest(source_commit="abc123")
    second = build_manifest(source_commit="abc123")
    assert first == second
    assert first["source_commit"] == "abc123"
    assert first["schema_version"] == "rpos.public-export.rc-evidence.v0.2"
    assert first["file_count"] == len(first["files"])
    assert first["files"] == sorted(first["files"], key=lambda item: item["path"])


def test_public_export_includes_product_surface_and_excludes_private_roots() -> None:
    manifest = build_manifest(source_commit="abc123")
    paths = {item["path"] for item in manifest["files"]}
    required = {
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SUPPORT.md",
        "CODE_OF_CONDUCT.md",
        "product-status.json",
        "formal/lean/lakefile.toml",
        "formal/lean/lean-toolchain",
        "site/index.html",
        "site/ja.html",
        "site/demo.html",
        "site/styles.css",
        "site/app.js",
        "tests/test_field_acceptance.py",
        "tests/test_cli_bom.py",
        "tools/build_public_export_manifest.py",
    }
    assert required <= paths
    assert not any(path.startswith(".github/") for path in paths)
    for root in manifest["excluded_roots"]:
        assert not any(path == root or path.startswith(root + "/") for path in paths)
    for path in manifest["excluded_relative_paths"]:
        assert path not in paths
