<!-- RPOS-DOC-ID: RPOS-COMPAT-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../ja/backward-compatibility-policy.md -->

# RPOS Backward Compatibility Policy

## Purpose

RPOS follows the freshest verified implementation, primary references, toolchains, and security/release practices available as of the change date, with 2026-08-12 as the current baseline for this release work, while avoiding needless breakage of already-supported alpha artifacts and workflows.

This does not mean freezing old behavior forever. The goal is to preserve a safe continuation or migration path without weakening the current responsibility boundary.

## Compatibility classification

A material change is classified as one of:

- `backward_compatible`: supported existing inputs, persisted state, CLI/API use, packet/templates, and evidence workflows continue to work;
- `compatibility_adapter_required`: a newer representation, schema, or behavior is introduced while a reader, alias, adapter, or migration path preserves supported prior use;
- `breaking_change_human_gate`: compatibility cannot be preserved safely and an explicit breaking-change review is required with affected versions, migration notes, Residual Owner, and Human Return Point.

## 0.1.0a1 compatibility baseline

The current alpha reader accepts previously supported `OperationDefinition` payloads that may predate these optional fields:

- `resume_authority`;
- `requires_human_gate`;
- `verification_required`.

When absent, the reader uses compatibility-preserving defaults:

- `resume_authority` -> `residual_owner`;
- `requires_human_gate` -> `false`;
- `verification_required` -> `true`.

Opening supported persisted state must not destructively rewrite the stored definition merely because the current reader understands additional optional fields.

This boundary is exercised by `tests/test_backward_compatibility.py`.

## Relationship to current references

RPOS may adopt newer standards, guidelines, schemas, toolchains, dependencies, and security practices. Each material update should still check:

1. whether supported persisted state and machine-readable inputs remain readable;
2. whether CLI/API or exported-evidence meaning changes silently;
3. whether compatibility that could be preserved with an adapter is being turned into an unnecessary breaking change;
4. whether historical evidence remains reconstructable rather than being overwritten by current values;
5. whether an unavoidable breaking change is returned to the Human Gate.

## Improvement requests and extensions

A capability or external integration that is not present in the current alpha is not automatically classified as permanently impossible. It may be evaluated as a feature request, integration request, Industry Profile, or compatibility request when it can be added without weakening the responsibility and product-quality boundaries.

Accepting a request for review is not a promise to implement it, and roadmap language is not a delivery guarantee unless explicitly stated otherwise.

## Japan-first / world-quality

Initial adoption material, reference packages, and guideline mappings prioritize Japanese organizations and enterprises, industry/economic bodies, public-sector users, and individual practitioners. API semantics, evidence discipline, formal boundaries, release engineering, and compatibility semantics remain designed for internationally reviewable technical quality.

## Not Proven

This policy does not guarantee indefinite compatibility with every future release, compatibility with arbitrary third-party adapters, production readiness, legal/regulatory compliance, or certification.
