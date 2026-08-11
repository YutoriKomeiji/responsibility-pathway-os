# RPOS Repair / Resume Slice Detailed Design v0.1

Status: Private RPP Detailed Design Candidate

## Objective

Add an explicit repair-preparation and authority-gated resume path after `REPAIR_REQUIRED` without allowing repair, restart, or mere capability to redispatch an external operation automatically.

## Normative requirements

- `INV-AUTH-001`: capability does not imply permission.
- `INV-RESP-001`: unresolved responsibility retains a residual owner and Human Return Point.
- `INV-RESTART-001`: restart or repair processing must not silently create a replacement dispatch.
- `INV-RESUME-001`: only the declared resume authority may return a repaired operation to dispatch-eligible state.
- `INV-RESUME-002`: resume authorization does not itself dispatch; a fresh explicit dispatch call with a new attempt identity is required.

## Data model change

Add `resume_authority` to `OperationDefinition`.

Compatibility rule for private-alpha persisted data: when deserializing an older record without `resume_authority`, fall back to `residual_owner`. New records should set it explicitly when the distinction matters.

Add `READY_TO_RESUME` to `OperationState`.

## State behavior

```text
REPAIR_REQUIRED
  -- prepare_repair by residual_owner --> READY_TO_RESUME
READY_TO_RESUME
  -- resume by resume_authority --> AUTHORIZED
AUTHORIZED
  -- explicit fresh dispatch --> DISPATCHING
```

No method in this slice calls an operation adapter except the existing explicit `dispatch()` method.

## Authority behavior

### prepare_repair

Preconditions:
- current state is `REPAIR_REQUIRED`;
- actor equals `residual_owner`;
- non-empty repair summary is supplied.

Effects:
- record bounded `repair_prepared` evidence;
- transition to `READY_TO_RESUME`;
- keep Human Return information visible.

### resume

Preconditions:
- current state is `READY_TO_RESUME`;
- actor equals `resume_authority`.

Effects:
- record explicit resume authorization through normal transition evidence;
- transition to `AUTHORIZED` only;
- do not create an attempt and do not call an adapter.

## Human Return

`READY_TO_RESUME` remains unresolved. Its Human Return package should identify the declared `resume_authority` as the authority required for the next state transition.

## Fresh dispatch requirement

After resume, dispatch follows the normal `AUTHORIZED -> DISPATCHING` path. A caller must supply a fresh `attempt_id` and `idempotency_key`. Existing attempt identities remain durable history and are not silently reused.

## Failure / ambiguity behavior

- wrong residual owner: reject without state change;
- empty repair summary: reject without state change;
- wrong resume authority: reject without state change;
- restart while `READY_TO_RESUME`: state remains unresolved; no automatic resume or dispatch;
- duplicate historical attempt key: existing idempotency behavior still prevents silent duplicate dispatch.

## Verification plan — Tier A

Focused tests:

1. only residual owner may prepare repair;
2. repair preparation enters `READY_TO_RESUME` and retains Human Return;
3. only resume authority may resume;
4. resume returns to `AUTHORIZED` without adapter invocation;
5. explicit fresh dispatch after resume can complete;
6. restart while ready-to-resume preserves the state and performs no dispatch;
7. prior idempotency key is not silently reused by resume.

GitHub Actions are not required for this development unit.

## IP / provenance note

This slice is derived from the existing RPR repair/resume and Human Return lineage plus RPOS authority/ambiguity invariants. It deliberately avoids third-party certificate, assurance-packet, replay-ledger, or proprietary terminology/structures.
