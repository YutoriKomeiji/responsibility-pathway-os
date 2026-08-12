<!-- RPOS-DOC-ID: RPOS-TEMPLATE-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../ja/responsibility-packet-templates.md -->

# Responsibility State Envelope Templates

RPOS provides reusable machine-readable **Responsibility State Envelope** templates for recurring responsibility handoffs. An envelope prepares and transports responsibility-relevant context for review, verification, repair, resumption, dependency evidence, evaluation evidence, and Human Return.

The earlier alpha term `ResponsibilityPacket` and the `rpos.packet.v0.1` wire identifier remain supported for backward compatibility. They are compatibility names, not the preferred public product terminology.

## Critical boundary

A valid envelope has `authority_effect: "none"`.

Completing, validating, storing, or transmitting an envelope does **not** authorize an operation, dispatch an operation, establish external effect, move an operation to `VERIFIED` or `COMPLETED`, or restore resume authority. Those effects require the corresponding RPOS state transition and authorized actor.

## Included template kinds

- `operation_proposal`
- `human_gate_decision`
- `verification_contract`
- `repair_plan`
- `resume_authorization`
- `dependency_evidence`
- `external_evaluation_evidence`
- `human_return_packet`

The catalog is stored at `templates/catalog.json`.

## Validation behavior

`rpos.validate_envelope(...)` is the preferred API and is strict by design:

- unknown envelope fields are rejected;
- unknown payload fields are rejected for the selected template kind;
- missing required fields are rejected;
- required string fields cannot be empty;
- unsupported template kinds and schema versions are rejected;
- any `authority_effect` other than `none` is rejected.

`rpos.validate_packet(...)` remains as a backward-compatible alias.

This fail-closed behavior protects the boundary between **prepared responsibility context** and **actual authority/state change**.

## Suggested adoption flow

1. copy the relevant template from `templates/catalog.json`;
2. replace placeholders using neutral organizational roles;
3. validate the envelope;
4. attach or record supporting evidence where applicable;
5. present the envelope to the actual responsible role or Human Gate;
6. perform any authority-bearing state transition through the RPOS service/CLI, not through the envelope itself;
7. preserve unresolved questions, Residual Owner, and Human Return Point when the pathway remains open.

## Evidence separation

Dependency evidence and external evaluation evidence are intentionally distinct from authorization and external-effect verification. An envelope may carry those evidence classes, but it cannot convert them into authority or operational completion.

## Compatibility

The current preferred schema identifier is `rpos.responsibility-state-envelope.v0.1`. The earlier `rpos.packet.v0.1` identifier is accepted so existing alpha artifacts remain readable. This compatibility support does not change the authority-neutral semantics.

## Not Proven

Template validation does not prove factual truth, completeness of supplied evidence, legal sufficiency, regulatory compliance, authorization legitimacy, external-system behavior, or production safety.
