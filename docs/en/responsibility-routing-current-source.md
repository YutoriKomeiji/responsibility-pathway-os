# Responsibility Routing — current-source semantic alignment

## Status

Current-source development note. Responsibility Routing is included in the published `0.1.0a3` line; this file records source-level semantics that continue to be aligned across the Responsibility Pathway stack. It does not promote the `0.1.0a4` candidate, create a new release, or claim production/enterprise readiness.

## Core rule

RPOS must not treat every blocked, failed, uncertain, or interrupted state as a Human Return.

Human Return is one bounded Responsibility Route. Other legitimate outcomes can include:

- continued autonomous work within explicit delegation;
- AI resolution within explicit delegation;
- hold for reconciliation;
- neutral hold while receiver eligibility is unresolved;
- organizational or institutional return;
- an authorized process route;
- stop and preserve unresolved residue.

## Non-propagation rules

RPOS should preserve these distinctions across runtime, restart, repair, readback, and handoff:

- `fail closed` != Human Gate;
- evidence transfer != Authority transfer;
- receiver capability != receiver eligibility;
- route selection != Authority grant;
- state recovery != approval or resume Authority recovery;
- readback success != permission to redispatch;
- Human Return = bounded Responsibility Route, not a generic fallback.

A receiver is eligible only when the relevant delegation/Authority scope, unresolved payload, evidence access, intervention capacity, and timing are sufficient for that route.

## Uncertain effects

For consequential external effects, uncertainty remains explicit until a bounded readback, reconciliation, repair, or authorized route transition resolves it.

If the external effect is unknown, RPOS must not infer failure from transport failure and must not redispatch merely because an execution mechanism remains available.

A reconciliation result may resolve effect state without granting new execution or resume Authority.

## Route envelope

A source-level route representation should be able to preserve at least:

- route identity and route kind;
- current/residual owner;
- receiver identity where applicable;
- receiver eligibility basis;
- Authority and delegation scope;
- unresolved payload;
- evidence/provenance references;
- allowed next actions;
- prohibited assumptions;
- reevaluation or closure conditions;
- timing/deadline where material.

The envelope is responsibility state, not an Authority token.

## Falsification / non-necessity

RPOS is not required merely because an AI system exists. If a host platform or application-specific design already preserves the same responsibility contract across ambiguous effects, authorization, readback, repair/resume, routing, and restart boundaries, adding RPOS may provide little or no additional value.

That is a valid integration conclusion.

## Assurance boundary

Executable tests, cross-runtime probes, and Lean 4 theorems are scoped evidence only.

They do not establish:

- real-world correctness of arbitrary integrations;
- legal or institutional Authority;
- universal receiver eligibility;
- implementation-wide formal conformance;
- production/enterprise readiness.

Published artifacts, repository `main`, unreleased source, historical evidence, and control documents must remain distinguishable. Exact-head validation and post-merge/readback are required before declaring a source transition closed, and a new release still requires its separate Human Gate.
