# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable


def sha256_file(path: str | Path) -> str:
    target = Path(path)
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_hash_bundle(files: Iterable[str | Path], *, source_commit: str) -> dict[str, object]:
    entries = []
    for value in sorted((Path(item).resolve() for item in files), key=lambda item: item.name):
        if not value.is_file():
            raise FileNotFoundError(value)
        entries.append({"name": value.name, "size": value.stat().st_size, "sha256": sha256_file(value)})
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":"))
    return {
        "format_version": 1,
        "created_at": datetime.now(UTC).isoformat(),
        "source_commit": source_commit,
        "artifacts": entries,
        "bundle_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an RPOS release artifact SHA-256 bundle.")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", default="release-hashes.json")
    args = parser.parse_args()
    Path(args.output).write_text(
        json.dumps(create_hash_bundle(args.files, source_commit=args.source_commit), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
