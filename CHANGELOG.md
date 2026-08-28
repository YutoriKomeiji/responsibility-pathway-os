# Changelog

All notable public-alpha changes to RPOS are recorded here.

RPOS uses pre-release versions while the public API and operational contracts are still being field-tested. Entries distinguish shipped behavior from deferred work.

## [0.1.0a1] - Unreleased

### Added
- Executable responsibility pathway from proposal through Human Gate, authorization, dispatch, effect verification, uncertainty, repair, explicit resume, and completion.
- SQLite-backed durable responsibility state and event history.
- Fail-closed handling for unknown external effect and adapter/reconciliation exceptions.
- Responsibility State Envelope templates with no implicit authority effect.
- Responsibility Observatory, evidence/provenance helpers, security primitives, CLI, and executable examples.
- Commit-time authority revalidation with exact target/effect binding, authority-epoch currentness, freshness, and one-shot consumption checks as an additive opt-in security primitive.
- Bounded Lean 4 evidence for state, reachability, evidence, packet/envelope, operational, and transparency boundaries.
- Deterministic public-export verification, wheel/sdist clean-install checks, SBOM generation, and release-candidate workflow.

### Release boundary
- This version is an Early Public Alpha / Executable Preview for engineering evaluation and bounded pilots.
- It does not claim unattended production readiness, legal/compliance certification, universal safety, or implementation-wide formal correctness.

### Deferred
- Production workload/capacity objectives.
- Multi-tenant isolation.
- Generic integration trust enforcement.
- External cryptographic integrity anchors.
- Mandatory adoption of newer security primitives across all legacy paths.
- Recurring post-release security revalidation and broader field portability evidence.
