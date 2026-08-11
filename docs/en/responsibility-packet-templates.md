<!-- RPOS-DOC-ID: RPOS-TEMPLATE-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../ja/responsibility-packet-templates.md -->

# Responsibility Packet Templates

RPOS provides reusable machine-readable packet templates for recurring responsibility handoffs. They help teams prepare consistent inputs for review, verification, repair, resumption, dependency evidence, evaluation evidence, and Human Return.

## Critical boundary

A valid packet has `authority_effect: "none"`.

Completing, validating, storing, or transmitting a packet does **not** authorize an operation, dispatch an operation, establish external effect, move an operation to `VERIFIED` or `COMPLETED`, or restore resume authority. Those effects require the corresponding RPOS state transition and authorized actor.

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

`rpos.validate_packet(...)` is strict by design:

- unknown envelope fields are rejected;
- unknown payload fields are rejected for the selected template kind;
- missing required fields are rejected;
- required string fields cannot be empty;
- unsupported template kinds and schema versions are rejected;
- any `authority_effect` other than `none` is rejected.

This fail-closed behavior protects the boundary between **prepared responsibility information** and **actual authority/state change**.

## Suggested adoption flow

1. copy the relevant packet from `templates/catalog.json`;
2. replace placeholders using neutral organizational roles;
3. validate the packet;
4. attach or record supporting evidence where applicable;
5. present the packet to the actual responsible role or Human Gate;
6. perform any authority-bearing state transition through the RPOS service/CLI, not through the packet itself;
7. preserve unresolved questions, Residual Owner, and Human Return Point when the pathway remains open.

## Evidence separation

Dependency evidence and external evaluation evidence are intentionally distinct from authorization and external-effect verification. A packet may carry those evidence classes, but it cannot convert them into authority or operational completion.

## Not Proven

Template validation does not prove factual truth, completeness of supplied evidence, legal sufficiency, regulatory compliance, authorization legitimacy, external-system behavior, or production safety.
