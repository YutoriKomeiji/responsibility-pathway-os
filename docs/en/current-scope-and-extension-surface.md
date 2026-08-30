<!-- RPOS-DOC-ID: RPOS-CURRENT-SCOPE-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1.0a2 -->
<!-- RPOS-DOC-STATUS: public-alpha-published -->
<!-- RPOS-DOC-COUNTERPART: ../ja/current-scope-and-extension-surface.md -->

# Current Scope and Extension Surface

RPOS 0.1.0a2 is a published Early Public Alpha / Executable Preview for preserving responsibility pathways in executable form. It states what works today while treating unsupported areas as reviewable extension surfaces rather than as permanently closed limitations.

## What works today

RPOS currently provides at least:

- authorization boundaries with Human Gate handling;
- durable responsibility state and event/audit history;
- separation between dispatch attempts and external effects;
- uncertainty preservation through `EFFECT_UNKNOWN`;
- observation-only reconciliation;
- `REPAIR_REQUIRED -> READY_TO_RESUME` with explicit resume authorization;
- Residual Owner / Human Return Point handling;
- bounded evidence import and provenance;
- Responsibility State Envelope templates with no implicit authority effect;
- CLI and runnable examples;
- wheel / sdist build and clean-install verification;
- CycloneDX 1.6 SBOM, artifact hash bundle, dependency audit, and secret scan;
- six published Lean 4 responsibility invariants machine-checked in declared bounded models and cross-linked to Python runtime tests; and
- current-main production-grade operational demos using the shipped RPOS service, separate localhost HTTP process, separate external-effect SQLite store, real process restart, reconciliation, repair/resume, and Human Gate denial paths.

The production-grade demo suite was added to `main` after the published `0.1.0a2` wheel/sdist. It is executable evidence for the current source tree and does not retroactively become part of the already-published package artifact.

## Current constraints are extension surfaces

At the alpha stage, external adapters, industry profiles, organization-specific rules, evidence sources, deployment topologies, and stronger delivery/effect guarantees may require additional design for each environment.

RPOS does not treat all such areas as permanent "cannot do" statements. After requirements and evidence boundaries are reviewed, a request may become:

1. a general capability that can be safely added to core;
2. a compatibility adapter or migration reader;
3. an Industry Profile or organization profile requirement;
4. an external adapter or integration boundary;
5. an area where qualified judgment or a Human Gate must remain;
6. a research/issue item that cannot yet be generalized safely.

## Improvement and integration requests

RPOS is designed to receive improvement requests from adopters, organizations, researchers, and developers as future design input.

Requests are especially useful for:

- new integrations and adapters;
- evidence/profile requirements from Japanese enterprises, industry bodies, and public-sector users;
- compatibility with existing workflows;
- additional recovery, reconciliation, and resume scenarios;
- audit, internal-control, and procurement outputs;
- developer ergonomics, CLI, API, and packaging improvements;
- invariants or counterexamples that should become formalization targets.

Accepting a request does not promise implementation, schedule, conformity, or safety. Candidate changes are evaluated against authority, evidence, compatibility, security, and public-claim boundaries.

## Backward compatibility

RPOS follows the freshest verified specifications, toolchains, and official references available at the time of a material change. Updates must not silently break previously supported alpha artifacts or adopter workflows.

Compatibility impact is classified as one of:

- `backward_compatible`;
- `compatibility_adapter_required`;
- `breaking_change_human_gate`.

When a breaking change is necessary, the affected versions/artifacts, migration path, claim impact, Residual Owner, and Human Return Point are recorded.

## Japan-first, world-reviewable

Initial adoption work prioritizes Japanese organizations and enterprises, economic and industry bodies, national/local public-sector users, and individual practitioners, engineers, and researchers.

That is a development direction, not a claim of adoption by those groups. Core semantics, formal evidence, security/release engineering, package quality, terminology, and evidence discipline are maintained so they can be inspected internationally. Public technical material is maintained in synchronized Japanese/English surfaces where practical.

## Claim boundary and promotion

RPOS does not need to understate capabilities that are actually implemented and verified. Where implementation, tests, and formal evidence support them, terms such as `runtime`, `operating system`, `formal`, `machine-checked`, `assurance`, `security`, and `evidence` may be used with their supporting scope.

Public boundaries are classified rather than flattened into one disclaimer list:

- **Current Evidence Boundaries** may move when scoped, reviewable evidence satisfies declared promotion criteria and the corresponding public claim is explicitly promoted;
- **Permanent Responsibility Boundaries** do not disappear merely through product maturity because they belong to qualified humans, institutions, integrators, external systems, or other responsibility layers.

The normative product direction remains [RPOS Operational Product Experience](operational-product-experience.md): the Public Alpha is an implemented core slice of that Operational System direction, not a redefinition of RPOS as a generic library.
