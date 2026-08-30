# Changelog

All notable public-alpha changes to RPOS are recorded here.

RPOS uses pre-release versions while the public API and operational contracts are still being field-tested. Entries distinguish shipped behavior from deferred work and preserve historical release provenance.

## [0.1.0a2] - 2026-08-29

Published to PyPI as `responsibility-pathway-os==0.1.0a2` via GitHub Actions Trusted Publishing.

### Changed
- Strengthened first-answer public semantics around the project identity: RPOS is an independently engineered Responsibility Pathway OS, not merely a Python helper package or a model wrapper.
- Made the public Python × Lean 4 architecture explicit across package metadata, README surfaces, GitHub Pages, product status, and Formal Assurance catalog.
- Added a clear Responsibility Pathway lineage from Model / Paper through Design, Engineering, Runtime, and RPOS, while keeping external authority separate from project evidence.
- Reframed public wording so implemented and verified facts are stated directly, goals are presented as goals, and proof/evidence ceilings remain adjacent to the claims they constrain.
- Synchronized machine-readable post-publication state for `0.1.0a2` while preserving `0.1.0a1` as an immutable previously published PyPI artifact.
- Updated release validation so the exact requested release identity remains fail-closed and re-publication of an already-published version is rejected by publication-state checks.

### Published artifacts
- Wheel: `responsibility_pathway_os-0.1.0a2-py3-none-any.whl` — SHA256 `83251e34ce847858b4a93535d1f309abdb125587d1b4d184876cce76203f9a31`.
- Source distribution: `responsibility_pathway_os-0.1.0a2.tar.gz` — SHA256 `614472025540db6c4dff228d0ab49d1160b24668c0bb940d5352b078f2915ea2`.
- PyPI reports Trusted Publishing for both files; public metadata reports Python `>=3.11` and MIT licensing.

### Verification carried forward
- Python/SQLite executable responsibility state and Human Gate paths.
- Eight executable evaluation scenarios.
- Exact-HEAD public-export and source-bound release evidence.
- Windows and Ubuntu compatibility checks on Python 3.11 and 3.12.
- Lean 4 Formal Assurance Surface with six named machine-checked responsibility invariants cross-linked to Python runtime tests, model scope, and proof ceilings.
- GitHub Pages validation with machine-checked assurance and verified architecture visuals.

### Release boundary
- `0.1.0a2` remains an Early Public Alpha / Executable Preview for engineering evaluation and bounded pilots.
- The named Lean 4 invariants are machine-checked in their declared bounded models; this does not by itself establish complete Python implementation conformance, deployment correctness, legal responsibility, or organizational authority.
- Production readiness and broader empirical/operational claims remain evidence-limited promotion targets rather than implied outcomes of a version bump.

## [0.1.0a1] - 2026-08-29

Published to PyPI as `responsibility-pathway-os==0.1.0a1` via GitHub Actions Trusted Publishing.

### Added
- Executable Responsibility Pathway OS runtime in Python/SQLite from proposal through Human Gate, authorization, dispatch, external-effect verification, uncertainty, repair, explicit resume, and completion.
- SQLite-backed durable responsibility state and event history.
- Fail-closed handling for unknown external effect and adapter/reconciliation exceptions.
- Responsibility State Envelope templates with no implicit authority effect.
- Responsibility Observatory, evidence/provenance helpers, security primitives, CLI, and executable examples.
- Commit-time authority revalidation with exact target/effect binding, authority-epoch currentness, freshness, and one-shot consumption checks as an additive opt-in security primitive.
- Lean 4 Formal Assurance Surface for selected responsibility invariants, including six public machine-checked assertions cross-linked to executable Python runtime tests, model scope, source identity, and proof ceilings.
- Deterministic public-export verification, wheel/sdist clean-install checks, SBOM generation, and release workflow.

### Release boundary
- This version is an Early Public Alpha / Executable Preview for engineering evaluation and bounded pilots.
- The named Lean 4 invariants are machine-checked in their declared abstract models; this does not by itself establish full Python implementation conformance.
- It does not claim unattended production readiness, legal/compliance certification, universal safety, or implementation-wide formal correctness.

### Deferred
- Production workload/capacity objectives.
- Multi-tenant isolation.
- Generic integration trust enforcement.
- External cryptographic integrity anchors.
- Mandatory adoption of newer security primitives across all legacy paths.
- Recurring post-release security revalidation and broader field portability evidence.
