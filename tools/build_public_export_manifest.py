# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "PUBLIC-EXPORT-EVIDENCE.json"

PUBLIC_ROOT_FILES = {
    "LICENSE",
    "README.md",
    "README.ja.md",
    "SECURITY.md",
    "SECURITY.ja.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SUPPORT.md",
    "CODE_OF_CONDUCT.md",
    "product-status.json",
    "pyproject.toml",
}
PUBLIC_ROOT_DIRS = {
    "docs",
    "examples",
    "formal",
    "provenance",
    "site",
    "specs",
    "src",
    "templates",
    "tests",
    "tools",
}


def _tracked_files() -> list[str]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return sorted(item.decode("utf-8") for item in output.split(b"\0") if item)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest(*, source_commit: str) -> dict:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    excluded_roots = set(baseline["excluded_roots"])
    excluded_paths = set(baseline["excluded_relative_paths"])
    files: list[dict] = []

    for rel in _tracked_files():
        path = Path(rel)
        if rel == BASELINE.name or rel.startswith(".github/"):
            continue
        if path.parts[0] in excluded_roots or rel in excluded_paths:
            continue
        if len(path.parts) == 1:
            if rel not in PUBLIC_ROOT_FILES:
                continue
        elif path.parts[0] not in PUBLIC_ROOT_DIRS:
            continue

        absolute = ROOT / path
        files.append({
            "bytes": absolute.stat().st_size,
            "path": rel,
            "sha256": _sha256(absolute),
        })

    included_paths = {item["path"] for item in files}
    forbidden = sorted(
        rel for rel in _tracked_files()
        if Path(rel).parts[0] in excluded_roots or rel in excluded_paths
    )
    leaked = [path for path in forbidden if path in included_paths]
    if leaked:
        raise RuntimeError(f"private boundary leak: {leaked}")

    return {
        "schema_version": "rpos.public-export.rc-evidence.v0.2",
        "source_commit": source_commit,
        "release_candidate": baseline["release_candidate"],
        "target_repository": baseline["target_repository"],
        "excluded_roots": baseline["excluded_roots"],
        "excluded_relative_paths": baseline["excluded_relative_paths"],
        "publication_non_claims": baseline["publication_non_claims"],
        "file_count": len(files),
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    manifest = build_manifest(source_commit=args.source_commit)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {manifest['file_count']} public-export files for {args.source_commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
