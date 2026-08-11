# RPOS Japan Audit Evidence Package v0.1

Status: Private RPP Engineering Profile / Japan-first

## Purpose

Provide a compact, machine-readable responsibility audit package suitable for Japanese enterprise, administrative, procurement, and internal-control review without collapsing distinct evidence classes into one success log.

The package is generated read-only from durable RPOS operation state and event history.

## Schema

Schema identifier: `rpos.audit.v0.1`.

Top-level fields:

- `operation_id`;
- `current_state`;
- `admission_decision`;
- `operation_definition`;
- separated `evidence` groups;
- `state_history`;
- `unresolved_responsibility`;
- `not_proven`.

## Evidence groups

### `authority_and_admission`

Contains proposal/admission evidence and explicit Human Gate decisions.

It answers who proposed the operation, whether a Human Gate was required, and what authority transition was recorded.

### `evaluation`

Contains external safety/capability evaluation evidence.

This evidence may inform responsible review but does not create authorization or verify an external effect.

### `execution_and_receipt`

Contains durable dispatch-start transitions and adapter receipts/results.

A successful receipt remains distinct from external-effect verification.

### `external_effect_readback`

Contains reconciliation/readback observations used to determine whether a declared external effect is verified, not applied, or unresolved.

### `recovery_and_resume`

Contains repair preparation, restart recovery, and explicit resume authorization evidence.

This group must not be interpreted as a successful original execution.

## State history

All state-transition events are retained separately as `state_history` so an auditor can reconstruct lifecycle order without treating the transition record itself as evidence that the real-world effect occurred.

## Unresolved responsibility

When the current operation remains unresolved, `unresolved_responsibility` carries the current Human Return package, including:

- Human Return Point;
- residual owner;
- required authority;
- unresolved reason.

A null value means only that the current RPOS state does not require a Human Return package; it does not prove the operation is safe, lawful, or correct outside the declared RPOS semantics.

## Not-Proven floor

The v0.1 package always states that the following are not proven by the package alone:

- legal or regulatory compliance;
- general AI safety;
- external-system correctness;
- production readiness;
- real-world effects beyond the declared readback scope.

Future Japanese guideline mappings may add bounded claim metadata but must not remove this floor without a reviewed schema revision.

## CLI surface

```text
rpos --db <database> audit <operation_id>
```

The command MUST be read-only. Generating an audit package must not recover, reconcile, approve, resume, dispatch, or otherwise mutate the operation.

## Japan-first use

The package is intended to become the common export boundary for:

- AI operations review;
- internal audit;
- procurement evidence;
- incident/recovery review;
- AI Guidelines for Business evidence mapping;
- later international profile mapping.

International mappings remain secondary to stabilizing the Japanese operational and accountability vocabulary.

## Not Proven

This document and package do not establish legal compliance, official certification, audit sufficiency for every organization, production readiness, or correctness of upstream evaluation systems or external services.
