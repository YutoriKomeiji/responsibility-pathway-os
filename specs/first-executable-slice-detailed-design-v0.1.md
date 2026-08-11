# RPOS First Executable Slice Detailed Design v0.1

Status: Private RPP Detailed Design Candidate

Depends on:
- `system-architecture-v0.1.md`
- `system-architecture-v0.1-internal-review.md`

## 1. Scope

Implement the smallest vertical slice that proves RPOS can exist as runnable software with durable responsibility state, Human Gate, dispatch/readback separation, unresolved-state preservation, restart reconstruction, and Human Return.

No network service, MCP mutation, plugin discovery, or production packaging is required in this slice.

## 2. Package layout

```text
incubator/rpos/
  src/rpos/
    __init__.py
    models.py
    service.py
    storage.py
    adapters.py
  tests/
    test_first_slice.py
```

## 3. State model

```text
PROPOSED
  -> HUMAN_GATE
  -> AUTHORIZED
  -> DISPATCHING
  -> EFFECT_UNKNOWN
  -> VERIFIED
  -> REPAIR_REQUIRED
  -> COMPLETED
  -> DENIED
  -> ABORTED
```

Allowed first-slice transitions:

- PROPOSED -> HUMAN_GATE
- PROPOSED -> AUTHORIZED
- PROPOSED -> DENIED
- HUMAN_GATE -> AUTHORIZED
- HUMAN_GATE -> DENIED
- AUTHORIZED -> DISPATCHING
- DISPATCHING -> VERIFIED
- DISPATCHING -> EFFECT_UNKNOWN
- DISPATCHING -> REPAIR_REQUIRED
- EFFECT_UNKNOWN -> VERIFIED
- EFFECT_UNKNOWN -> REPAIR_REQUIRED
- VERIFIED -> COMPLETED
- REPAIR_REQUIRED -> AUTHORIZED only through explicit repair/resume in a later slice; first slice does not expose this transition.
- any non-terminal non-dispatching state -> ABORTED only when policy permits; first slice keeps abort internal/not exposed unless needed by tests.

`COMPLETED`, `DENIED`, and `ABORTED` are terminal in the first slice.

## 4. Data contracts

### OperationDefinition

Fields:
- `operation_id: str`
- `action_name: str`
- `requested_by: str`
- `execution_actor: str`
- `approval_authority: str | None`
- `human_return_point: str`
- `residual_owner: str`
- `requires_human_gate: bool`
- `verification_required: bool`

### AdmissionDecision

Enum:
- `ALLOW`
- `HUMAN_GATE`
- `DENY`

The first control-plane policy is intentionally simple:
- if `requires_human_gate` is true -> HUMAN_GATE;
- otherwise -> ALLOW.

No capability field grants permission.

### AttemptRecord

Fields:
- `attempt_id`
- `operation_id`
- `idempotency_key`
- `dispatch_started: bool`
- `dispatch_finished: bool`
- `receipt_status: str | None`
- `readback_verified: bool | None`
- `result_reason: str | None`

### AdapterResult

Fields:
- `receipt_status`: `SUCCEEDED | FAILED | UNKNOWN`
- `receipt`: mapping
- `readback_verified: bool | None`
- `readback`: mapping
- `reason: str | None`

Rules:
- `receipt_status=SUCCEEDED` with `readback_verified=True` may reach VERIFIED.
- `receipt_status=FAILED` reaches REPAIR_REQUIRED.
- all other combinations reach EFFECT_UNKNOWN.
- successful receipt without verified readback never reaches VERIFIED.

### HumanReturnPackage

Fields:
- `operation_id`
- `state`
- `human_return_point`
- `residual_owner`
- `required_authority`
- `summary`
- `unresolved_reason`

This is intentionally compact and is not a ledger dump.

## 5. Storage

SQLite tables:

### operations
- operation_id TEXT PRIMARY KEY
- definition_json TEXT NOT NULL
- state TEXT NOT NULL
- admission_decision TEXT NOT NULL
- updated_at TEXT NOT NULL

### attempts
- attempt_id TEXT PRIMARY KEY
- operation_id TEXT NOT NULL
- idempotency_key TEXT NOT NULL
- dispatch_started INTEGER NOT NULL
- dispatch_finished INTEGER NOT NULL
- receipt_status TEXT
- readback_verified INTEGER
- result_reason TEXT
- UNIQUE(operation_id, idempotency_key)

### events
- seq INTEGER PRIMARY KEY AUTOINCREMENT
- operation_id TEXT NOT NULL
- event_type TEXT NOT NULL
- actor TEXT NOT NULL
- payload_json TEXT NOT NULL
- created_at TEXT NOT NULL

First slice uses one SQLite connection per service instance. Concurrency hardening is deferred.

## 6. Boot and restart

`RposService(database_path)` opens the database and initializes schema.

`boot_report()` returns:
- schema available;
- operation count;
- unresolved operation IDs.

Unresolved states for boot report:
- HUMAN_GATE
- DISPATCHING
- EFFECT_UNKNOWN
- REPAIR_REQUIRED

A service restart never auto-dispatches an unresolved operation.

If an operation is found in DISPATCHING with an attempt whose dispatch has started but does not have a persisted terminal result, it is normalized to EFFECT_UNKNOWN during explicit `recover_incomplete_dispatches()`, not automatically at constructor time. The recovery operation records an event.

This preserves a distinction between boot/read-only reconstruction and mutating recovery.

## 7. Service interface

### propose(definition)
- reject duplicate operation ID unless definition is byte/field equivalent in a later idempotency feature; first slice rejects duplicates.
- run admission policy.
- persist PROPOSED then transition to HUMAN_GATE / AUTHORIZED / DENIED.

### approve(operation_id, actor)
- allowed only from HUMAN_GATE.
- actor must equal `approval_authority`.
- transition to AUTHORIZED.

### dispatch(operation_id, attempt_id, idempotency_key, adapter)
Preconditions:
- state AUTHORIZED;
- actor semantics use `execution_actor` from definition in first slice service-internal call;
- create durable attempt before adapter call;
- transition AUTHORIZED -> DISPATCHING before effect dispatch.

Execution:
- call adapter once;
- persist result;
- classify result;
- transition to VERIFIED / EFFECT_UNKNOWN / REPAIR_REQUIRED;
- if VERIFIED, transition immediately to COMPLETED.

Idempotency:
- repeated `(operation_id, idempotency_key)` returns prior persisted result/state without adapter redispatch when a finished attempt exists.
- if the prior attempt started but outcome is incomplete/unknown, do not redispatch; return current unresolved state.

### inspect(operation_id)
Returns definition, state, latest attempt summary, and compact Human Return package when state requires human attention.

### list_unresolved()
Returns operation IDs in Human Gate / dispatch-uncertain / repair-required states.

### recover_incomplete_dispatches()
For each DISPATCHING operation with an incomplete attempt, transition to EFFECT_UNKNOWN and record restart/recovery evidence. Never redispatch.

## 8. Transition enforcement

All transitions go through one transition function with an explicit allowed-transition table. Direct store mutation is private to storage/recovery implementation and must not be exposed as a public service method.

## 9. Invariant mapping

- INV-AUTH-001 -> `propose` policy and absence of capability-as-permission path.
- INV-AUTH-002 -> `approve` authority equality check and dispatch requiring AUTHORIZED.
- INV-EXEC-001 -> `classify_adapter_result` requires verified readback for VERIFIED.
- INV-EVID-001 -> VERIFIED only when `readback_verified is True` if verification is required.
- INV-UNK-001 -> unknown/missing readback maps to EFFECT_UNKNOWN.
- INV-RESP-001 -> every definition requires `human_return_point` and `residual_owner`; unresolved inspection exposes both.
- INV-RESTART-001 -> incomplete DISPATCHING recovery maps to EFFECT_UNKNOWN without adapter call.

## 10. Tier-A focused tests

Required before the first slice is accepted:

1. gated operation cannot dispatch before approval;
2. wrong approval authority is rejected;
3. successful receipt without verified readback becomes EFFECT_UNKNOWN;
4. successful receipt with verified readback becomes COMPLETED;
5. adapter failure becomes REPAIR_REQUIRED;
6. repeated idempotency key after persisted success does not redispatch;
7. incomplete DISPATCHING state is recoverable after service restart without redispatch;
8. unresolved inspection retains Human Return Point and residual owner.

These tests are intended for direct local execution. GitHub Actions are not required for the inner-loop acceptance of this slice.

## 11. Lean timing

Do not block this first executable implementation on Lean proof completion. Stabilize the transition model and executable tests first. Then add a Lean model mapped to the invariant IDs without claiming it proves the Python implementation.
