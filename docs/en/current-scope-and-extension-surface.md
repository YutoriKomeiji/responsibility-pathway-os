<!-- RPOS-DOC-ID: RPOS-CURRENT-SCOPE-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1.0a1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../ja/current-scope-and-extension-surface.md -->

# Current Scope and Extension Surface

RPOS 0.1.0a1 is an early public alpha for preserving responsibility pathways in executable form. It states what works today while treating unsupported areas as reviewable extension surfaces rather than as permanently closed limitations.

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
- responsibility packet templates;
- CLI and runnable examples;
- wheel / sdist build and clean-install verification;
- CycloneDX 1.6 SBOM, artifact hash bundle, dependency audit, and secret scan;
- bounded machine-checked Lean 4 formal evidence.

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

With 2026-08-12 as the current program baseline, RPOS follows the freshest verified specifications, toolchains, and official references available at the time of a material change. Updates must not silently break previously supported alpha artifacts or adopter workflows.

Compatibility impact is classified as one of:

- `backward_compatible`;
- `compatibility_adapter_required`;
- `breaking_change_human_gate`.

When a breaking change is necessary, the affected versions/artifacts, migration path, claim impact, Residual Owner, and Human Return Point are recorded.

## Japan-first, world-quality

Initial adoption prioritizes Japanese organizations and enterprises, economic and industry bodies, national/local public-sector users, and individual practitioners, engineers, and researchers.

At the same time, core semantics, formal evidence, security/release engineering, package quality, terminology, and evidence discipline are maintained at a level suitable for international technical review. Even when Japanese material is designed first, product, adoption, operations, profile, review, value, release, and public technical documentation is maintained as synchronized Japanese/English pairs within the same change.

## Claim boundary and promotion

RPOS does not need to understate capabilities that are actually implemented and verified. Where implementation, tests, and formal evidence support them, terms such as `runtime`, `operating system`, `formal`, `verified`, `assurance`, `security`, and `evidence` may be used with their supporting scope.

Public boundaries are classified rather than flattened into one disclaimer list:

- **evidence-limited boundaries** may move when scoped, reviewable evidence satisfies declared promotion criteria and the corresponding public claim is explicitly promoted;
- **permanent responsibility boundaries** do not disappear merely through product maturity because they belong to qualified humans, institutions, integrators, external systems, or other responsibility layers.

This distinction exists so an adopter can see both the current evidence-backed capability surface and the route by which a temporary boundary can move, without confusing that route with responsibilities RPOS must not appropriate.

See [Claim Boundary Promotion](claim-boundary-promotion.md) for the current criteria, evidence owners, and promotion states. The normative product direction remains [RPOS Operational Product Experience](operational-product-experience.md): the Public Alpha is an implemented core slice of that Operational System direction, not a redefinition of RPOS as a generic library.
