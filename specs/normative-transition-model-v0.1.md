# RPOS Normative Transition Model v0.1

Status: Private RPP Normative Model Candidate

## Purpose

Define the first compact state-transition semantics shared conceptually by the executable runtime, focused conformance tests, and Lean 4 formalization.

This model is intentionally smaller than the Python implementation. It specifies responsibility-relevant state semantics, not storage format, adapter implementation, database correctness, network behavior, or organizational/legal responsibility.

## States

- `PROPOSED`
- `HUMAN_GATE`
- `AUTHORIZED`
- `DISPATCHING`
- `EFFECT_UNKNOWN`
- `VERIFIED`
- `REPAIR_REQUIRED`
- `READY_TO_RESUME`
- `COMPLETED`
- `DENIED`
- `ABORTED`

## Normative transitions

```text
PROPOSED -> HUMAN_GATE
PROPOSED -> AUTHORIZED
PROPOSED -> DENIED
HUMAN_GATE -> AUTHORIZED
HUMAN_GATE -> DENIED
AUTHORIZED -> DISPATCHING
DISPATCHING -> VERIFIED
DISPATCHING -> EFFECT_UNKNOWN
DISPATCHING -> REPAIR_REQUIRED
EFFECT_UNKNOWN -> VERIFIED
EFFECT_UNKNOWN -> REPAIR_REQUIRED
VERIFIED -> COMPLETED
REPAIR_REQUIRED -> READY_TO_RESUME
READY_TO_RESUME -> AUTHORIZED
```

No other transition is normative in v0.1.

## Responsibility semantics

### Authorization

`AUTHORIZED` means the operation is eligible for explicit dispatch under the declared authority model. It does not mean the external operation has started or succeeded.

### Dispatching

`DISPATCHING` means an execution attempt has been durably associated with the operation and external execution may have begun. The state is unresolved until outcome classification is available.

### Effect unknown

`EFFECT_UNKNOWN` means available evidence is insufficient to determine whether the intended external effect exists. Receipt success may still lead here when independent verification is required and absent.

### Verified

`VERIFIED` means the declared verification contract has supplied sufficient positive evidence for the intended external effect. It is a bounded runtime verification state, not a universal truth or legal conclusion.

### Repair required

`REPAIR_REQUIRED` means the operation cannot continue through the normal completion path without explicit responsible repair work.

### Ready to resume

`READY_TO_RESUME` means repair preparation is recorded, but execution authority has not yet been restored. It is unresolved and Human Return-visible.

### Completed

`COMPLETED` is reachable only after `VERIFIED` in this model.

## Core invariants

- `INV-AUTH-001`: only `AUTHORIZED` may transition directly to `DISPATCHING`.
- `INV-GATE-001`: `HUMAN_GATE` may not transition directly to `DISPATCHING`.
- `INV-VERIFY-001`: execution/receipt does not by itself entail `VERIFIED`.
- `INV-COMPLETE-001`: `COMPLETED` is reached only from `VERIFIED`.
- `INV-UNKNOWN-001`: `EFFECT_UNKNOWN` is distinct from `VERIFIED` and `COMPLETED`.
- `INV-REPAIR-001`: `REPAIR_REQUIRED` cannot transition directly to `AUTHORIZED`; repair preparation must produce `READY_TO_RESUME` first.
- `INV-RESUME-001`: `READY_TO_RESUME` is not equivalent to `AUTHORIZED`.
- `INV-RESUME-002`: resume authorization changes `READY_TO_RESUME -> AUTHORIZED`; it does not dispatch.
- `INV-RESP-001`: unresolved states remain externally inspectable with a responsible return path in the executable implementation.

## Runtime mapping

The Python `OperationState` names map one-to-one to this v0.1 normative state set. The runtime `_ALLOWED` transition map is expected to conform to the normative transition list above.

Runtime-specific details outside the formal model include:

- SQLite transaction behavior;
- exact event payloads;
- attempt/idempotency persistence;
- adapter exception classification;
- CLI serialization;
- timestamps;
- concrete actor strings and identity resolution.

## Formal proof boundary

Lean proofs over this model may establish properties of this declared transition relation. They do not prove:

- Python implementation correctness;
- SQLite correctness or durability guarantees under every failure mode;
- external adapter/service behavior;
- cybersecurity of the host system;
- real-world safety;
- legal/regulatory compliance;
- organizational responsibility;
- completeness or truth of supplied evidence.

## Conformance direction

The next conformance layer should mechanically compare executable state transitions against this normative relation using shared scenario IDs. A later release gate may require:

1. Python tests;
2. normative conformance scenarios;
3. Lean compilation/proofs for declared invariants;
4. operational integration evidence.

None substitutes for another.
