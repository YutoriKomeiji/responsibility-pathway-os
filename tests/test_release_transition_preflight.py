from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "check_release_transition.py"


def write_fixture(
    root: Path,
    *,
    version: str,
    publication_state: str,
    latest_published: str,
    readme_current: str,
    changelog: str,
) -> None:
    (root / "pyproject.toml").write_text(
        "[project]\nname = \"responsibility-pathway-os\"\n"
        f"version = \"{version}\"\n",
        encoding="utf-8",
    )
    (root / "product-status.json").write_text(
        json.dumps(
            {
                "version": version,
                "publication_state": publication_state,
                "latest_published_version": latest_published,
                "production_ready": False,
                "release_gate": {"explicit_human_gate_required": True},
            }
        ),
        encoding="utf-8",
    )
    for name in ("README.md", "README.ja.md"):
        (root / name).write_text(readme_current, encoding="utf-8")
    (root / "CHANGELOG.md").write_text(changelog, encoding="utf-8")


def candidate_readme(version: str) -> str:
    return (
        f"<!-- RPOS-DOC-VERSION: {version} -->\n"
        f"Version: **{version}** — release candidate / not yet published.\n"
        f"python -m pip install responsibility-pathway-os=={version}\n"
    )


def published_readme(version: str) -> str:
    return (
        f"<!-- RPOS-DOC-VERSION: {version} -->\n"
        f"Version: **{version}** — current published release.\n"
        f"python -m pip install responsibility-pathway-os=={version}\n"
    )


def run_check(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_candidate_requires_future_version_identity_before_publication(tmp_path: Path) -> None:
    write_fixture(
        tmp_path,
        version="0.1.0a5",
        publication_state="not_published",
        latest_published="0.1.0a4",
        readme_current=candidate_readme("0.1.0a5"),
        changelog="## [0.1.0a5] - candidate\nNot published.\n",
    )
    result = run_check(
        tmp_path,
        "--mode",
        "candidate",
        "--version",
        "0.1.0a5",
        "--latest-published",
        "0.1.0a4",
    )
    assert result.returncode == 0, result.stderr


def test_candidate_rejects_stale_previous_version_as_active_document_identity(tmp_path: Path) -> None:
    write_fixture(
        tmp_path,
        version="0.1.0a5",
        publication_state="not_published",
        latest_published="0.1.0a4",
        readme_current=published_readme("0.1.0a4"),
        changelog="## [0.1.0a5] - candidate\nNot published.\n",
    )
    result = run_check(
        tmp_path,
        "--mode",
        "candidate",
        "--version",
        "0.1.0a5",
        "--latest-published",
        "0.1.0a4",
    )
    assert result.returncode != 0
    assert "missing required marker" in (result.stderr + result.stdout)


def test_candidate_rejects_premature_publication_state(tmp_path: Path) -> None:
    write_fixture(
        tmp_path,
        version="0.1.0a5",
        publication_state="pypi_published",
        latest_published="0.1.0a5",
        readme_current=candidate_readme("0.1.0a5"),
        changelog="0.1.0a5\n",
    )
    result = run_check(
        tmp_path,
        "--mode",
        "candidate",
        "--version",
        "0.1.0a5",
        "--latest-published",
        "0.1.0a4",
    )
    assert result.returncode != 0
    assert "publication_state='not_published'" in (result.stderr + result.stdout)


def test_candidate_rejects_readme_that_claims_candidate_is_current_public(tmp_path: Path) -> None:
    write_fixture(
        tmp_path,
        version="0.1.0a5",
        publication_state="not_published",
        latest_published="0.1.0a4",
        readme_current=published_readme("0.1.0a5") + "candidate\n",
        changelog="0.1.0a5 candidate; not published.\n",
    )
    result = run_check(
        tmp_path,
        "--mode",
        "candidate",
        "--version",
        "0.1.0a5",
        "--latest-published",
        "0.1.0a4",
    )
    assert result.returncode != 0
    assert "forbidden pre-publication claim" in (result.stderr + result.stdout)


def test_post_publish_requires_public_state_to_match(tmp_path: Path) -> None:
    write_fixture(
        tmp_path,
        version="0.1.0a5",
        publication_state="pypi_published",
        latest_published="0.1.0a5",
        readme_current=published_readme("0.1.0a5"),
        changelog="Published responsibility-pathway-os==0.1.0a5\n",
    )
    result = run_check(
        tmp_path,
        "--mode",
        "post-publish",
        "--version",
        "0.1.0a5",
    )
    assert result.returncode == 0, result.stderr
