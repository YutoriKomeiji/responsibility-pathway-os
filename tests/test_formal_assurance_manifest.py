# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_formal_assurance_manifest_crosswalk_is_resolvable(tmp_path: Path) -> None:
    output = tmp_path / "formal-assurance.json"
    source_commit = "a" * 40
    subprocess.run(
        [
            sys.executable,
            "tools/build_formal_assurance_manifest.py",
            "--source-commit",
            source_commit,
            "--output",
            str(output),
        ],
        check=True,
    )
    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "rpos.formal-assurance.manifest.v0.1"
    assert manifest["source_commit"] == source_commit
    assert manifest["lean"]["machine_checked"] is False
    assert manifest["assertion_count"] >= 6
    assert manifest["evidence_role"] == "public_assurance_not_runtime_authority"
    for item in manifest["assertions"]:
        assert item["lean"]["source_sha256"]
        assert item["runtime_tests"]
        assert all(test["source_sha256"] for test in item["runtime_tests"])
        assert item["proof_ceiling"]["en"]
        assert item["proof_ceiling"]["ja"]
