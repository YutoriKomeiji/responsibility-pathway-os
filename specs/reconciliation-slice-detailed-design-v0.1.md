# RPOS Reconciliation Slice Detailed Design v0.1

Status: Private RPP Detailed Design Candidate

## Objective

Add a bounded reconciliation path for operations in `EFFECT_UNKNOWN` without redispatching the original external operation.

This slice is independently derived from RPOS invariants and the existing RPR ambiguity/reconciliation lineage. It does not adopt third-party assurance-packet, certificate, replay-ledger, or proprietary terminology.

## Normative requirements

- `INV-UNK-001`: unknown external effect remains unresolved until reconciliation or explicit bounded repair resolves it.
- `INV-RESP-001`: unresolved state retains residual owner and Human Return Point.
- `INV-RESTART-001`: reconciliation must not silently redispatch an unresolved prior attempt.
- `INV-EVID-001`: transition to VERIFIED requires positive readback/reconciliation evidence under the declared contract.

## Reconciliation interface

A reconciliation strategy is observational. It receives the operation ID and latest persisted attempt metadata and returns one of:

- `VERIFIED_APPLIED` — independent observation supports that the intended external effect exists;
- `VERIFIED_NOT_APPLIED` — independent observation supports that the intended effect does not exist;
- `UNRESOLVED` — evidence remains insufficient.

The strategy interface has no dispatch method and receives no authority to repeat the operation.

## Authority

For the first slice, reconciliation is callable only by the operation's `residual_owner`.

This is intentionally conservative. Later designs may introduce a distinct reconciliation authority, but capability must not imply permission.

## State behavior

```text
EFFECT_UNKNOWN
  -- VERIFIED_APPLIED --> VERIFIED --> COMPLETED
  -- VERIFIED_NOT_APPLIED --> REPAIR_REQUIRED
  -- UNRESOLVED --> EFFECT_UNKNOWN
```

`UNRESOLVED` records new evidence but performs no state transition.

## Evidence behavior

Every reconciliation attempt records:

- observer/reconciliation actor;
- reconciliation status;
- bounded evidence payload;
- reason;
- source attempt reference when available.

The event is operational evidence. It is not claimed to be externally immutable, legally dispositive, or formal proof.

## Failure behavior

If the reconciliation strategy raises an exception, classify the result as `UNRESOLVED`, record the exception class as a bounded reason, retain `EFFECT_UNKNOWN`, and return Human Return information.

No exception path may call the original operation adapter.

## Verification plan — Tier A

Focused tests:

1. wrong actor cannot reconcile;
2. verified-applied completes without redispatch;
3. verified-not-applied requires repair;
4. unresolved stays unknown;
5. reconciliation exception stays unknown;
6. original operation adapter call count does not increase during reconciliation;
7. Human Return remains present for unresolved/repair states.

GitHub Actions are not required for this development unit.
