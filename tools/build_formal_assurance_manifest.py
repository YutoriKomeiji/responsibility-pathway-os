#!/usr/bin/env python3
"""Build a source-bound RPOS formal-assurance manifest.

This tool validates that every public assurance entry points to an existing
Lean theorem and executable pytest selector. It never treats formal evidence as
runtime authority; it packages the cross-layer evidence surface for review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "formal" / "assurance-catalog.json"
TOOLCHAIN = ROOT / "formal" / "lean" / "lean-toolchain"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_catalog() -> dict[str, object]:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("schema_version") != "rpos.formal-assurance.catalog.v0.1":
        raise SystemExit("unsupported formal-assurance catalog schema")
    assertions = data.get("assertions")
    if not isinstance(assertions, list) or not assertions:
        raise SystemExit("formal-assurance catalog must contain assertions")
    return data


def _validate_test_selector(selector: str) -> dict[str, str]:
    if "::" not in selector:
        raise SystemExit(f"runtime test selector must use path::test_name: {selector}")
    path_text, test_name = selector.split("::", 1)
    path = ROOT / path_text
    if not path.is_file():
        raise SystemExit(f"runtime test file missing: {path_text}")
    text = path.read_text(encoding="utf-8")
    if re.search(rf"^def\s+{re.escape(test_name)}\s*\(", text, flags=re.MULTILINE) is None:
        raise SystemExit(f"runtime test function missing: {selector}")
    return {"selector": selector, "source_sha256": _sha256(path)}


def _validate_theorem(module_text: str, theorem: str) -> str:
    local_name = theorem.rsplit(".", 1)[-1]
    if re.search(rf"^theorem\s+{re.escape(local_name)}\b", module_text, flags=re.MULTILINE) is None:
        raise SystemExit(f"Lean theorem missing: {theorem}")
    return local_name


def build(source_commit: str, machine_checked: bool) -> dict[str, object]:
    if HEX40.fullmatch(source_commit) is None:
        raise SystemExit("--source-commit must be a lowercase 40-character Git SHA")
    catalog = _load_catalog()
    output_assertions: list[dict[str, object]] = []
    ids: set[str] = set()

    for raw in catalog["assertions"]:  # type: ignore[index]
        if not isinstance(raw, dict):
            raise SystemExit("assurance assertion must be an object")
        assurance_id = str(raw.get("id", ""))
        if not assurance_id or assurance_id in ids:
            raise SystemExit(f"invalid or duplicate assurance id: {assurance_id!r}")
        ids.add(assurance_id)

        lean = raw.get("lean")
        if not isinstance(lean, dict):
            raise SystemExit(f"{assurance_id}: lean mapping missing")
        module_text = str(lean.get("module", ""))
        theorem = str(lean.get("theorem", ""))
        module = ROOT / module_text
        if not module.is_file():
            raise SystemExit(f"{assurance_id}: Lean module missing: {module_text}")
        source = module.read_text(encoding="utf-8")
        _validate_theorem(source, theorem)

        selectors = raw.get("runtime_tests")
        if not isinstance(selectors, list) or not selectors:
            raise SystemExit(f"{assurance_id}: at least one runtime test is required")
        tests = [_validate_test_selector(str(selector)) for selector in selectors]

        output_assertions.append(
            {
                **raw,
                "lean": {
                    "module": module_text,
                    "theorem": theorem,
                    "source_sha256": _sha256(module),
                    "machine_checked": machine_checked,
                },
                "runtime_tests": tests,
            }
        )

    toolchain = TOOLCHAIN.read_text(encoding="utf-8").strip()
    if not toolchain:
        raise SystemExit("Lean toolchain is empty")

    return {
        "schema_version": "rpos.formal-assurance.manifest.v0.1",
        "product_version": catalog["product_version"],
        "source_commit": source_commit,
        "evidence_role": "public_assurance_not_runtime_authority",
        "lean": {
            "toolchain": toolchain,
            "machine_checked": machine_checked,
            "build_command": "cd formal/lean && lake build",
        },
        "catalog_sha256": _sha256(CATALOG),
        "assertion_count": len(output_assertions),
        "assertions": output_assertions,
        "proof_ceiling": {
            "en": "Lean checks only the declared abstract models. Runtime implementation, SQLite durability, external systems, evidence truth, organizational authority, legal conclusions, universal exactly-once behavior, and deployment safety require separate evidence.",
            "ja": "Lean が機械検証するのは宣言された抽象モデルだけです。runtime implementation、SQLite durability、external system、evidence の真偽、organizational authority、法的結論、universal exactly-once、deployment safety には別の evidence が必要です。",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--machine-checked", action="store_true")
    args = parser.parse_args()
    manifest = build(args.source_commit, args.machine_checked)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(f"formal assurance manifest: {manifest['assertion_count']} assertions -> {output}")


if __name__ == "__main__":
    main()
