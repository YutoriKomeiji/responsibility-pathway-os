<!-- RPOS-DOC-ID: RPOS-PRODUCT-EXPERIENCE-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: normative-product-direction -->
<!-- RPOS-DOC-COUNTERPART: ../ja/operational-product-experience.md -->

# RPOS Operational Product Experience

## Purpose

RPOS is developed as an **Operational System**, not as a model, chatbot, generic library, or general agent-orchestration framework. Models and agents may propose work. RPOS owns the responsibility-bearing transition from proposal to authorized operation, external-effect verification, recovery, resumption, and completion.

The release target is therefore stronger than a developer-installable alpha: a user should be able to install RPOS, start it with safe defaults, understand why work is proceeding or stopped, recover from uncertainty, and return later without losing unresolved responsibility.

This document is the normative product direction. An early Public Alpha may implement only part of this experience, but a partial release does not redefine the product into a generic Python library. Product maturity should move toward this direction while preserving the core invariants below.

## Core invariants — must not drift

These define RPOS even before the complete Product Shell exists:

- **RPOS owns operation, not intelligence.** Models and agents are replaceable proposal sources, not authority sources.
- A proposal, model statement, or transport receipt is not operational authority or verified external effect.
- Human Gate, authority, target, effect, evidence, and context remain explicit responsibility-bearing boundaries.
- Uncertain external effects remain uncertain; they are not converted into false success or blind retry.
- Restart, reconciliation, repair, and resume preserve unresolved responsibility instead of erasing it.
- Repair readiness does not silently restore execution authority; resume requires an explicit authorized path.
- Residual Owner and Human Return Point remain visible when responsibility cannot be closed automatically.
- Read-only observability does not mutate authority or responsibility state.

A change that violates these invariants is not ordinary product evolution. It requires explicit architectural review because it changes what RPOS is.

## 0.1.0a1 implemented slice

The 0.1.0a1 Public Alpha implements an operational core slice of this direction, including:

- durable responsibility states and event history;
- Human Gate and authorization boundaries;
- dispatch-attempt / external-effect separation;
- `EFFECT_UNKNOWN` uncertainty preservation;
- crash-consistent state/event persistence and restart recovery;
- observation-only reconciliation;
- repair, explicit resume authorization, and Human Return paths;
- Residual Owner / Human Return Point structures;
- commit-time authority revalidation for an opt-in exact effect/target binding;
- evidence/provenance surfaces, executable examples, CLI/package surfaces, and bounded Lean evidence;
- a public Product Site and browser state-path explorer that explains the lifecycle without pretending simulation is Python-runtime execution.

This slice supports the Public Alpha claim. It is not yet the complete Operational Product Experience.

## Post-alpha product targets

The following remain product-direction targets rather than reasons to redefine the current core as a library:

- Product Shell / Observatory that answers operational questions without requiring internal-code knowledge;
- safe local-first service/runtime defaults and startup diagnostics;
- one-click installer, with Windows as the initial target unless later evidence changes priority;
- normal first use without requiring Git/Python knowledge;
- operational-evidence backup/export;
- update, rollback, and uninstall strategy;
- optional model/provider connections after safe local first boot;
- broader supported Effect Adapters and field-validated deployment profiles;
- reusable operational memory across approvals, evidence, unresolved ownership, policy, and recovery history.

Promotion of any of these targets into a public capability claim requires implementation and reviewable evidence; see [Claim Boundary Promotion](claim-boundary-promotion.md).

## Product promise

RPOS should progress through four user outcomes:

1. **Wow** — the user immediately sees that a receipt or model statement is not the same as a verified real-world effect.
2. **Useful** — bounded work can be completed without reading RPOS internals.
3. **Trust** — uncertainty, duplicate risk, and recovery are handled without false completion or silent authority expansion.
4. **Dependable** — approvals, evidence, unresolved ownership, policies, and recovery history accumulate into reusable operational memory.

## Architecture boundary

```text
User / Organization
        |
        v
RPOS Product Shell / Observatory
        |
        v
RPOS Operational Core
  - Policy / Authority
  - Human Gate
  - Responsibility State Envelope
  - Dispatch boundary
  - Evidence ledger
  - Reconciliation / Repair / Resume
  - Residual Owner / Human Return Point
        |
        +---- Model Adapter ---- LLM / Agent / Local Model
        |
        +---- Effect Adapter --- GitHub / Files / APIs / SaaS / other systems
```

RPOS owns **operation, not intelligence**. A model adapter is a replaceable proposal source. An external-effect adapter is a replaceable observation/dispatch boundary. Neither may bypass the RPOS state and evidence contracts.

## Model Adapter contract v0.1

A model or agent may propose structured intent such as:

```json
{
  "intent": "send_message",
  "target": "example-target",
  "requested_capability": "message.send",
  "proposal_summary": "Send the prepared status update"
}
```

This proposal is advisory input. It MUST NOT by itself:

- grant authority;
- satisfy a Human Gate;
- prove an external effect;
- convert `EFFECT_UNKNOWN` to `VERIFIED`;
- create `COMPLETED`;
- authorize retry or resume.

The adapter boundary should remain thin enough that OpenAI, Anthropic, Google, local models, and independent agent frameworks can be substituted without changing normative RPOS completion semantics.

## Effect Adapter contract v0.1

Effect adapters should expose bounded stages rather than one opaque `execute()` success claim:

`prepare -> dispatch -> receipt -> observe/readback -> verify -> reconcile -> repair -> resume`

Not every external system supports every stage directly. Missing capabilities must remain visible as gaps; they must not be synthesized from model confidence or transport success.

## Responsibility Observatory

The primary UI should answer operational questions, not only show logs:

- What pathway is active?
- What responsibility state is current?
- Who or what authority is required?
- Is a Human Gate waiting?
- What evidence is missing?
- Is external effect still uncertain?
- Who is the Residual Owner?
- Where is the Human Return Point?
- What action is allowed next?
- Why is retry/resume blocked?

Read-only observability MUST NOT mutate authority or responsibility state.

## First Experience target

A first-run bounded demonstration should intentionally include both success and uncertainty:

1. create/propose a safe local operation;
2. show required capability and Human Gate;
3. authorize and dispatch;
4. distinguish transport receipt from effect verification;
5. deliberately create an `EFFECT_UNKNOWN` case;
6. explain why RPOS refuses false completion or blind retry;
7. inspect/reconcile;
8. repair if required;
9. explicitly resume;
10. reach verified completion and show retained evidence.

The desired first-use outcome is not merely "the command worked" but "I understand why this Operational System is different."

## Installer/product-shell requirements

The intended product release surface should eventually provide:

- one-click installer, with Windows as the first target unless later evidence changes priority;
- local service/runtime and embedded database;
- safe local-only default configuration;
- no Git/Python requirement for normal first use;
- startup diagnostics and clear recovery guidance;
- backup/export of operational evidence;
- crash-safe continuation of unresolved pathways;
- update/uninstall strategy;
- optional model/provider connection after local first boot.

## Promotion and verification route

New product slices are incubated in RPP first:

`spec -> schema/model -> implementation -> executable tests -> Lean 4 bounded proof where applicable -> focused CI -> JA/EN docs -> promotion candidate`

Only then are verified files promoted into the standalone `responsibility-pathway-os` repository, where final standalone tests and packaging/install evidence become the release evidence source of truth.

RPP success alone is not standalone RPOS release evidence.

## Lean 4 product role

Lean 4 is a user-visible verification layer for small critical boundaries, not a decorative badge. RPOS should prefer readable theorems connected to concrete operational risks, pair them with executable tests, and state their proof ceiling.

Initial product-relevant theorem themes:

- a model proposal is not operational authority;
- a model report is not verified external effect;
- a transport receipt is not verified external effect;
- only verified work may complete;
- ready-to-resume is not authorized-to-resume;
- read-only observation cannot mutate responsibility state.

Beginner-oriented JA/EN material should explain these proofs using RPOS examples so that users can learn why formal verification is useful before learning advanced theorem-proving techniques.

## Claim boundary and promotion

This product direction does not make future targets current capabilities. Public claims advance only when implementation and scoped evidence support them.

Evidence-limited gaps such as broader deployment support, Product Shell maturity, installer quality, platform coverage, and implementation-wide conformance may move through declared promotion criteria. Permanent responsibility boundaries — legal authority, final organizational responsibility, correctness of arbitrary external systems, and unsupported universal exactly-once guarantees — do not disappear merely because RPOS matures.

See [Claim Boundary Promotion](claim-boundary-promotion.md) for the current evidence boundary, promotion criteria, evidence owners, and permanent responsibility boundaries.
