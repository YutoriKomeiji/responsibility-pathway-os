<!-- RPOS-DOC-ID: RPOS-OPS-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: incubator -->
<!-- RPOS-DOC-COUNTERPART: ../ja/development-and-document-sync-policy.md -->

# RPOS Development and Documentation Synchronization Policy v0.1

## Purpose

Prevent one-sided Japanese/English updates and missed propagation to related artifacts when changing RPOS implementation, specifications, adoption materials, operations materials, industry profiles, expert-review materials, and value-evidence materials.

This policy does not treat the mere existence of documents as completion. It establishes operating discipline for confirming that changed meaning has been propagated consistently to affected implementation, specifications, examples, operating guidance, and evidence materials.

## 1. Simultaneous Japanese and English creation

The following user-facing and operations-facing documents are created and updated as Japanese/English pairs in the same change unit by default.

- product and architecture explanations
- adoption guides and pilot procedures
- operations runbooks and incident/recovery/resume procedures
- explanatory documents for Industry Profiles
- explanatory documents for Expert Review Packs
- explanatory documents for Cost / Value Evidence
- installation, Quick Start, and release-readiness materials
- specifications and Best Practice documents intended for public or adopter use

The default process is not to write one language now and translate the other later. Semantic changes should be reflected in both languages in the same PR whenever practical.

### Exceptions

The following are not automatically subject to the bilingual-pair requirement, but must be paired when promoted or reused as product documentation.

- source code, tests, and machine-readable schemas
- raw verification evidence and execution logs
- temporary internal research notes and exploration records
- historical single-language incubator material

Existing single-language material is not bulk-translated retroactively. Substantive revision, productization, or promotion into adoption/operations material becomes the Human Return Point for pairing.

## 2. Language and document-control headers

Language rules are declared in headers rather than as body-language mandates. Paired documents contain at least:

- `RPOS-DOC-ID`
- `RPOS-DOC-LANG`
- `RPOS-DOC-VERSION`
- `RPOS-DOC-STATUS`
- `RPOS-DOC-COUNTERPART`

When a program or configuration file needs language/document-control metadata, use a header expressed in the valid comment syntax of that file format.

## 3. Pre-change Impact Scan

Work that changes RPOS semantics classifies impact before implementation or before opening the PR. At minimum, review the following propagation sets.

| Change class | Required propagation review |
|---|---|
| state / transition semantics | normative spec, README / Quick Start, Adoption Guide, Operations / Recovery / Resume Runbook, Industry Profiles, examples/tests, terminology |
| CLI / schema | README / CLI docs, examples, Adoption Guide, Profile / sample configuration, audit / evidence docs |
| Evidence model | audit package, guideline matrix, Expert Review Pack, Industry Profiles, relevant Cost / Value Evidence |
| Dependency / Adapter | supply-chain profile, Operations Runbook, audit / evidence, Industry Profiles |
| Recovery / Resume | Runtime semantics, Operations Runbook, Adoption Guide, expert-review triggers, Industry Profiles |
| Release / Package | installation docs, Quick Start, release readiness, Not Proven, security / credential boundary |

This table is a minimum set. Additional documents, tests, or examples must be reviewed when affected.

## 4. Documentation Propagation decision

A PR that changes RPOS meaning, use, or operation includes a `Documentation propagation` section.

Each related item is explicitly classified as one of:

- `updated`: updated in the same change
- `reviewed-not-affected`: reviewed and no semantic change is required
- `deferred`: intentionally not updated now; record an Issue, Residual Owner, reason, and Human Return Point

`not reviewed` and `probably unaffected` are not acceptable states.

## 5. Deferred propagation

Propagation may be deferred only when the deferral does not make the current change misleading and the following are preserved:

- linked issue
- residual owner
- unresolved reason
- affected document or artifact
- human return point

An unresolved synchronization gap in public/release-candidate material is treated as a release-readiness gap.

## 6. Bilingual-pair consistency

Automated validation checks registered pairs for:

- existence of both files
- matching Document ID
- matching Version
- matching Status
- correct `ja` / `en` language declarations
- reciprocal Counterpart references

Automation does not prove semantic translation equivalence. Semantic equivalence, terminology consistency, and aligned Not Proven boundaries remain review responsibilities.

## 7. Implementation/document synchronization order

Recommended small vertical slice:

`spec / profile -> model / schema -> service / read-only integration -> CLI -> tests -> JA/EN docs -> propagation scan -> focused verification -> audit -> merge -> issue evidence`

Documentation is not a decorative final step. When implementation changes user-facing meaning, documentation synchronization belongs to the same implementation unit.

## 8. Completion criteria

An RPOS change may be reported complete only when at least:

1. verification evidence exists for the target implementation/specification;
2. registered JA/EN pairs are structurally synchronized;
3. Documentation propagation has been decided;
4. deferred items preserve responsibility and a resume point;
5. incomplete propagation is not reported as complete.

## Not Proven

This policy and its automation do not prove:

- perfect semantic equivalence of translations
- legal or regulatory compliance
- technical correctness of document content
- completeness of the impact scan
- public/release readiness

Those require separate review, verification, and Human Gates.
