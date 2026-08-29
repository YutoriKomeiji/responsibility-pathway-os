<!-- RPOS-DOC-ID: RPOS-FORMAL-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-COUNTERPART: README.ja.md -->

# RPOS Lean 4 Formal Assurance — Responsibility Pathway invariants

RPOS is an executable Responsibility Pathway OS implemented in Python/SQLite. This directory contains the Lean 4 formal assurance layer that machine-checks selected structural responsibility invariants of the declared RPOS model.

The formal surface is designed to make three things simultaneously visible:

1. **what responsibility property is machine-checked;**
2. **which executable Python runtime test corresponds to that public assertion;**
3. **where the proof stops.**

The canonical public crosswalk is `../assurance-catalog.json`.

## Published machine-checked responsibility assertions

| Operational risk | Lean theorem | Meaning in the declared model |
| --- | --- | --- |
| Human decision state becomes execution authority | `RPOS.human_gate_cannot_dispatch_directly` | `HUMAN_GATE` cannot directly enter `DISPATCHING`. |
| Intermediate/transport success becomes completion | `RPOS.only_verified_enters_completed` | only `VERIFIED` may directly enter `COMPLETED`. |
| Ambiguous external effect is collapsed into success | `RPOS.effect_unknown_is_not_completed` | `EFFECT_UNKNOWN` is distinct from `COMPLETED`. |
| Repair readiness silently restores authority | `RPOS.ready_to_resume_is_not_authorized` | `READY_TO_RESUME` is distinct from `AUTHORIZED`. |
| API/transport receipt is treated as real-world effect proof | `RPOS.receipt_is_not_effect_verification` | a transport receipt is not external-effect-verification evidence. |
| Model output becomes authority by implication | `RPOS.model_proposal_is_not_authority` | a model proposal is not authorization-relevant evidence. |

These theorem names are intentionally domain-readable because they identify the exact responsibility property being checked; they are not marketing aliases for broader claims.

## Build

The project is pinned to Lean 4.32.2.

```bash
cd formal/lean
lake build
```

CI and release evidence run the same bounded formal project and generate an exact-source Formal Assurance manifest.

## Modules

- `RPOSState.lean` — state machine, Human Gate, completion, uncertainty, and resume-authority invariants.
- `RPOSReachability.lean` — bounded multi-step reachability and no-direct-shortcut results.
- `RPOSEvidenceBoundary.lean` — separation among authority-relevant, effect-verification, receipt, evaluation, and dependency evidence.
- `RPOSPacketBoundary.lean` — no-authority-effect properties for Responsibility State Envelopes / packets.
- `RPOSOperationalBoundary.lean` — model proposal, human authorization, transport receipt, external observation, and read-only observability boundaries.
- `RPOSTransparencyBoundary.lean` — transparency and evidence distinctions.

## Python × Lean 4 evidence architecture

RPOS does not use Lean as a decorative badge. Public Formal Assurance assertions are cross-linked to executable Python tests.

The evidence relation is:

```text
operational risk
  -> named Lean theorem
  -> machine-checked abstract invariant
  -> corresponding Python runtime test(s)
  -> source identity + model scope + proof ceiling
```

This is a crosswalk, not an automatic refinement proof between Lean and Python. The runtime tests exercise executable behavior independently; the Lean theorem establishes the named property in the declared formal model.

## What this formal layer proves

For each theorem, Lean proves the proposition stated by that theorem from the definitions and assumptions in the source module. The six public assertions therefore have machine-checked proof evidence for their declared abstract scope.

For example:

- Human Gate is structurally separated from direct dispatch;
- completion is structurally gated by `VERIFIED` in the direct-transition model;
- external-effect uncertainty remains distinct from completion;
- repair readiness remains distinct from authorization;
- transport receipts remain distinct from external-effect-verification evidence;
- model proposals remain distinct from operational authority.

## Proof ceiling

The formal layer does not by itself establish:

- full Python implementation conformance;
- truth or sufficiency of an arbitrary external observation;
- legitimacy of a concrete human authorization;
- correctness of SQLite, adapters, operating systems, networks, or external services;
- universal exactly-once behavior;
- production readiness, legal compliance, certification, or organizational authority.

Those are separate evidence or responsibility owners, not weaknesses hidden by the theorem names.

## Why the boundary is explicit

RPOS treats formal proof, executable implementation evidence, and operational external-effect evidence as distinct evidence classes. A stronger public claim may be promoted only when the missing bridge evidence is actually supplied and reviewed.

This keeps the public statement strong where the proof is strong, and narrow where the evidence is narrow.
