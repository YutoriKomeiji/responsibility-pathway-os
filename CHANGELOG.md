# Changelog

All notable public-alpha changes to RPOS are recorded here.

RPOS uses pre-release versions while the public API and operational contracts are still being field-tested. Entries distinguish shipped behavior from deferred work and preserve historical release provenance.

## [0.1.0a4] - candidate / not published

Hotfix candidate for the PyPI long-description version mismatch discovered immediately after `0.1.0a3` publication.

### Changed
- Package long description now uses a publication-neutral `PYPI_README.md` instead of the GitHub README's mutable "current published release" surface.
- Release tests fail closed if the PyPI long description does not contain the candidate version and exact install command.
- Wheel and sdist metadata validation now checks the rendered long description, not only package name and version fields.

### Candidate boundary
- Runtime behavior is unchanged from `0.1.0a3`; this candidate repairs package metadata / release-surface consistency.
- Current published PyPI version remains `0.1.0a3` until explicit Human Gates and exact-head validation complete for `0.1.0a4`.
- `0.1.0a3` remains in release history as the published artifact that exposed the metadata mismatch.

## [0.1.0a3] - 2026-09-18

Published as GitHub prerelease `v0.1.0a3` and to PyPI as `responsibility-pathway-os==0.1.0a3` after exact-head validation and explicit Human Gates.

### Added
- Additive Responsibility Routing classification through `ResponsibilityRoute`, `ResponsibilityRouteKind`, and `classify_responsibility_route` without replacing the existing v0.1 operation-state contract.
- Bounded route distinctions for Human Gate, reconciliation hold, repair, and return-for-authorization while preserving `route_selection != authority_grant`.
- Deterministic production-grade integration demos for supplier-payment ambiguity, deployment repair/resumption, and privileged-access denial.
- Release-transition preflight checks that fail closed on candidate/publication-state drift.

### Changed
- Strengthened current-source responsibility semantics so unresolved external effects are not automatically rounded into Human Return.
- Refined public/support surfaces and maturity wording while retaining existing proof, authority, and production-readiness ceilings.
- Preserved the distinction between repair readiness and resume Authority, receipt and verified external effect, evidence transfer and Authority transfer, and fail-closed behavior and Human Gate.
- Aligned RPOS release surfaces with the RPR public-alpha pattern: GitHub prerelease/tag carries source release identity and release notes; PyPI remains the package-distribution surface.

### Published artifacts
- Wheel: `responsibility_pathway_os-0.1.0a3-py3-none-any.whl` — SHA256 `64e497a5d5e1b280e8b1fcb14b0241cc0a6e17f5f429a4fbf3ab4e5799d8c159`.
- Source distribution: `responsibility_pathway_os-0.1.0a3.tar.gz` — SHA256 `1df85977f0d8170ec45e831b1a96e0a426d866e958909d1d1ea025008c877b76`.
- GitHub prerelease tag `v0.1.0a3` points to exact validated commit `7814959c7e42599b1824bc5101bb96f331d762ad`.
- PyPI publication used Trusted Publishing with digital attestations enabled.

### Release boundary
- `0.1.0a3` remains an Early Public Alpha for engineering evaluation and bounded pilots.
- GitHub prerelease publication and PyPI package publication are separate release surfaces; neither creates production readiness or Authority.
- No version bump creates legal or organizational Authority, universal safety, third-party correctness, production readiness, or implementation-wide formal correctness.

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
- This version remains an Early Public Alpha / Executable Preview for engineering evaluation and bounded pilots.
- The named Lean 4 invariants are machine-checked in their declared abstract models; this does not by itself establish full Python implementation conformance.
- It does not claim unattended production readiness, legal/compliance certification, universal safety, or implementation-wide formal correctness.

### Deferred
- Production workload/capacity objectives.
- Multi-tenant isolation.
- Generic integration trust enforcement.
- External cryptographic integrity anchors.
- Mandatory adoption of newer security primitives across all legacy paths.
- Recurring post-release security revalidation and broader field portability evidence.
