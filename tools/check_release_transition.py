from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path


class TransitionError(SystemExit):
    pass


def fail(message: str) -> None:
    raise TransitionError(message)


def load_project_version(root: Path) -> str:
    with (root / "pyproject.toml").open("rb") as fh:
        return tomllib.load(fh)["project"]["version"]


def load_status(root: Path) -> dict:
    return json.loads((root / "product-status.json").read_text(encoding="utf-8"))


def read_text(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def require(text: str, needle: str, *, where: str) -> None:
    if needle not in text:
        fail(f"{where}: missing required marker: {needle!r}")


def reject(text: str, pattern: str, *, where: str) -> None:
    if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
        fail(f"{where}: forbidden pre-publication claim matched: {pattern!r}")


def check_candidate(root: Path, candidate: str, latest_published: str) -> None:
    project_version = load_project_version(root)
    status = load_status(root)

    if project_version != candidate:
        fail(f"pyproject version mismatch: expected candidate={candidate}, actual={project_version}")
    if status.get("version") != candidate:
        fail(f"product-status version mismatch: expected candidate={candidate}, actual={status.get('version')}")
    if status.get("publication_state") != "not_published":
        fail(
            "candidate mode requires publication_state='not_published'; "
            f"actual={status.get('publication_state')!r}"
        )
    if status.get("latest_published_version") != latest_published:
        fail(
            "candidate mode must retain the previous public version until readback; "
            f"expected={latest_published!r}, actual={status.get('latest_published_version')!r}"
        )
    if status.get("production_ready") is not False:
        fail("candidate mode must not promote production_ready")
    gate = status.get("release_gate", {})
    if gate.get("explicit_human_gate_required") is not True:
        fail("candidate mode requires explicit_human_gate_required=true")

    changelog = read_text(root, "CHANGELOG.md")
    # Candidate may be documented, but it must not be described as already published.
    reject(
        changelog,
        rf"(?:published|released)\s+(?:to\s+PyPI\s+)?(?:as\s+)?`?responsibility-pathway-os=={re.escape(candidate)}`?",
        where="CHANGELOG.md",
    )

    for path in ("README.md", "README.ja.md"):
        text = read_text(root, path)
        require(text, latest_published, where=path)
        # In candidate mode, README may mention the candidate but must not call it the current published release.
        reject(
            text,
            rf"{re.escape(candidate)}[^\n]{{0,100}}(?:current published release|現在の公開版|PyPI公開済み|published package)",
            where=path,
        )


def check_post_publish(root: Path, published: str) -> None:
    project_version = load_project_version(root)
    status = load_status(root)

    if project_version != published:
        fail(f"pyproject version mismatch: expected published={published}, actual={project_version}")
    if status.get("version") != published:
        fail(f"product-status version mismatch: expected published={published}, actual={status.get('version')}")
    if status.get("publication_state") != "pypi_published":
        fail(
            "post-publish mode requires publication_state='pypi_published'; "
            f"actual={status.get('publication_state')!r}"
        )
    if status.get("latest_published_version") != published:
        fail(
            "post-publish mode requires latest_published_version to match public readback; "
            f"expected={published!r}, actual={status.get('latest_published_version')!r}"
        )

    changelog = read_text(root, "CHANGELOG.md")
    require(changelog, published, where="CHANGELOG.md")

    for path in ("README.md", "README.ja.md"):
        text = read_text(root, path)
        require(text, published, where=path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fail-closed checks for RPOS release transition state."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", choices=("candidate", "post-publish"), required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--latest-published")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.mode == "candidate":
        if not args.latest_published:
            fail("candidate mode requires --latest-published")
        check_candidate(root, args.version, args.latest_published)
    else:
        check_post_publish(root, args.version)

    print(
        f"release transition state verified: mode={args.mode}; version={args.version}; "
        f"latest_published={args.latest_published}"
    )


if __name__ == "__main__":
    main()
