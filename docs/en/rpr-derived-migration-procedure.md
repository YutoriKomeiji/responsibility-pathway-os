<!-- RPOS-DOC-ID: RPOS-MIGRATION-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: pre-migration-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../ja/rpr-derived-migration-procedure.md -->

# RPOS Migration Procedure — Derived from the RPR Standalone Export Path

Status: pre-migration procedure. This document does not authorize transfer or public release.

## Source procedure readback

This procedure is derived from the RPR release/export controls recorded in `incubator/rpr/docs/release-preparation-4.md` and the verified failure knowledge in `governance/failure-knowledge/incidents/FK-2026-002-standalone-export-integrity-gap.md`.

The governing lesson is that a standalone product repository is not merely a copied Python package directory. The exported boundary must contain every artifact needed to substantiate the public product claims and must be testable with private RPP paths unavailable.

## Preconditions

Before any RPP -> standalone RPOS transfer:

1. #191 pre-migration hardening is complete or every residual item is explicitly deferred with owner/reason/claim impact/Human Return Point.
2. #180 `MIGRATION_READY_0.1.0a1` criteria are satisfied.
3. One immutable RPP source commit SHA is selected.
4. The public-export allowlist/manifest is generated from that SHA and reviewed.
5. RPP-private research, internal chronology, credentials, unpublished-only material, and private comparison dossiers are excluded.
6. Public metadata is internally consistent: product name, repository, distribution, import package, version, license/SPDX, citation, security contact/boundary, and supported Python versions.

## Standalone inventory rule

The allowlist must enumerate the complete product evidence surface required for public claims, including as applicable:

- Python package/runtime source;
- CLI and executable examples;
- tests/fixtures required to substantiate published behavior;
- Lean source and pinned/declared formal verification path;
- formal-evidence and public-claim crosswalks;
- responsibility packet templates/catalog;
- EN/JA README, Quick Start, operational boundary, Not Proven, security/provenance documentation;
- package metadata/license;
- maintenance/validation tools required by standalone CI;
- release/export evidence files intended for public retention.

No required validator or test may depend on the private RPP directory layout after transfer.

## Transfer sequence

1. Freeze exact RPP source SHA.
2. Generate a clean export from the reviewed allowlist; do not copy an editable working tree wholesale.
3. Record the export manifest and source SHA together.
4. Populate the already-created private `YutoriKomeiji/responsibility-pathway-os` repository.
5. In the standalone repository, install from the standalone package boundary before running tests.
6. Run the complete standalone verification bundle with private RPP paths unavailable.
7. Compile Lean from the standalone formal boundary.
8. Run executable scenarios, focused tests, wheel build, isolated clean install, installed CLI/Quick Start, document-sync checks, and export/inventory checks.
9. Record artifact hashes and verification evidence from the same frozen source/export lineage.
10. If any required artifact is missing or any validator reaches back into RPP, classify the transfer as incomplete and repair the standalone inventory before proceeding.

## Product-quality gate inherited from RPR

RPOS must preserve at least the same release-quality discipline used for RPR, adapted to the RPOS product boundary.

One release candidate must be bound to one immutable source SHA and one package version. From that same lineage, retain a coherent evidence bundle containing, as applicable:

- clean-export manifest hash;
- wheel hash and source-distribution hash;
- CycloneDX SBOM or approved equivalent plus validation result;
- Lean 4 verification evidence and declared toolchain version;
- functional, integration, and end-to-end scenario results;
- wheel and source-distribution clean-install results from separate clean environments;
- installed CLI / Quick Start results;
- restart, reconciliation, repair, and explicit-resume evidence;
- secret-scan result;
- dependency / vulnerability-review result;
- release audit and claim/evidence review result;
- known limitations and accepted residual risks;
- artifact hash bundle.

Clean-install evidence must retain interpreter/toolchain version, platform, artifact SHA-256, installed package version, scenario results, and whether repository paths or user site-packages were present.

A candidate is invalid if its generated artifacts or evidence come from mixed commits, dirty/editable source states, or unrecorded manual substitutions.

Absence of required evidence is a `hold`, not implicit approval.

## Human Gate after private migration

Passing the migration verification only establishes that the private standalone repository is an internally coherent RPOS alpha candidate.

A separate Human Gate is still required before:

- changing repository visibility to public;
- creating a public tag/release;
- publishing to PyPI;
- enabling Pages/demo;
- external announcement/marketing;
- any production-readiness claim.

The Human Gate decision pack must contain source SHA/version, manifest and artifact hashes, SBOM status, clean-install/E2E results, security-review results, known limitations, accepted residual risks, and named decision/evidence/residual owners.

Permitted outcomes are `approve`, `approve_with_conditions`, or `hold`.

## RPOS-specific deviations from RPR

RPOS adds these required public surfaces beyond the generic RPR release path:

- explicit Lean theorem/property -> implementation/test -> assumption -> `not_proven` crosswalk;
- explicit claim/evidence crosswalk for authoritative terminology such as `Operating System`, `runtime`, `formal`, `verified`, `assurance`, and `security`;
- responsibility packet authority-boundary evidence;
- defensive-provenance snapshot preserving RPD -> RPE -> RPR -> RPOS lineage without exporting private third-party research.

These additions strengthen the standalone evidence boundary; they do not relax the RPR clean-export or product-quality rules.
