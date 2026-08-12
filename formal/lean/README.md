<!-- RPOS-DOC-ID: RPOS-FORMAL-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: README.ja.md -->

# RPOS Lean Formalization — Public Alpha Candidate

Status: machine-checked bounded formal model / Lean 4 CI verified

## Verification evidence

`RP-CYCLE-001` introduced the dedicated `RPOS Lean formal verification` workflow. The first successful run compiled the declared formal modules with Lean 4.32.2.

This evidence means that the theorem sources listed below are accepted by the configured Lean compiler for the declared abstract model. It does **not** prove the Python implementation, external systems, deployment, organizational behavior, or legal conclusions.

## Modules

- `RPOSState.lean` — normative responsibility states, direct transition relation, and local transition invariants.
- `RPOSReachability.lean` — bounded reflexive/transitive reachability witnesses and no-direct-shortcut properties for uncertainty, repair, resumption, and completion.
- `RPOSEvidenceBoundary.lean` — bounded separation between authorization-relevant evidence, effect-verification evidence, receipts, evaluations, and dependency/supply-chain evidence.
- `RPOSPacketBoundary.lean` — bounded separation properties for responsibility/evidence packets.
- `RPOSOperationalBoundary.lean` — product-facing model-independence boundary: model proposals are not authority or effect verification, receipts are not verified effects, and Observatory reads are non-mutating in the bounded command model.

## Direct-transition invariants

| Invariant | Lean theorem |
|---|---|
| only `AUTHORIZED` may directly enter `DISPATCHING` | `RPOS.only_authorized_enters_dispatching` |
| `HUMAN_GATE` cannot directly dispatch | `RPOS.human_gate_cannot_dispatch_directly` |
| only `VERIFIED` may directly enter `COMPLETED` | `RPOS.only_verified_enters_completed` |
| `REPAIR_REQUIRED` cannot directly become `AUTHORIZED` | `RPOS.repair_required_cannot_authorize_directly` |
| `READY_TO_RESUME` is distinct from `AUTHORIZED` | `RPOS.ready_to_resume_is_not_authorized` |
| resume does not directly dispatch | `RPOS.resume_does_not_dispatch_directly` |
| `EFFECT_UNKNOWN` is distinct from `COMPLETED` | `RPOS.effect_unknown_is_not_completed` |

## Reachability / repair-resume properties

| Property | Lean theorem |
|---|---|
| `AUTHORIZED` has the normative dispatch path | `RPOS.authorized_reaches_dispatching` |
| `EFFECT_UNKNOWN` has an explicit verification-to-completion witness | `RPOS.effect_unknown_has_verified_completion_path` |
| repair has an explicit readiness-to-reauthorization witness | `RPOS.repair_has_explicit_reauthorization_path` |
| `EFFECT_UNKNOWN` cannot directly complete | `RPOS.effect_unknown_cannot_complete_directly` |
| `REPAIR_REQUIRED` cannot directly dispatch | `RPOS.repair_required_cannot_dispatch_directly` |
| `READY_TO_RESUME` cannot directly complete | `RPOS.ready_to_resume_cannot_complete_directly` |
| `READY_TO_RESUME` restores authority through `AUTHORIZED` | `RPOS.ready_to_resume_restores_authority` |

The positive reachability theorems are **existence witnesses**, not liveness claims. For example, a theorem showing a path from `EFFECT_UNKNOWN` to `COMPLETED` does not claim every unresolved operation eventually completes.

## Evidence-class separation properties

The bounded evidence model proves that:

- safety-evaluation evidence is not authorization-relevant evidence;
- capability-evaluation evidence is not authorization-relevant evidence;
- dependency/supply-chain evidence is not authorization-relevant evidence;
- an execution receipt is not external-effect-verification evidence;
- safety/capability evaluation evidence is not external-effect-verification evidence;
- dependency evidence is not external-effect-verification evidence.

The model also marks authority-admission and recovery/resume evidence as authorization-relevant classes while explicitly stating that possessing evidence does not itself grant authority.

## Operational product boundary properties

`RPOSOperationalBoundary.lean` deliberately uses a very small teaching model so that the connection between a product risk and a theorem stays readable.

| Product risk | Lean theorem |
|---|---|
| model proposal is mistaken for operational authority | `RPOS.model_proposal_is_not_authority` |
| model proposal is mistaken for verified external effect | `RPOS.model_proposal_is_not_effect_verification` |
| transport receipt is mistaken for verified external effect | `RPOS.receipt_is_not_effect_verification` |
| read-only Observatory action mutates operational state | `RPOS.observatory_is_read_only` |

The positive witnesses in that module classify explicit human authorization as authorization-relevant and external observation as effect-verification-relevant. They do not claim that arbitrary evidence is truthful, sufficient, or legitimate in every deployment.

This module is intentionally approachable: it is suitable as a first Lean 4 example because the operational meaning can be understood before advanced proof techniques are needed.

## Evidence layers

RPOS keeps three evidence layers separate:

1. **Formal proof evidence** — Lean theorems over the explicitly declared abstract model.
2. **Executable implementation evidence** — Python tests and runnable examples over the current implementation.
3. **Operational effect evidence** — observation/readback of concrete external effects.

No layer may impersonate another.

## Not Proven

These Lean files do not prove:

- correctness or conformance of the Python implementation;
- correctness/durability of SQLite;
- external adapter/service behavior;
- exactly-once behavior over arbitrary external systems;
- security of a deployment environment;
- legal or regulatory compliance;
- patent non-infringement or freedom to operate;
- organizational responsibility or authority legitimacy;
- real-world AI/system safety;
- truth or completeness of runtime evidence;
- liveness or eventual completion for arbitrary operations.

Future cycles should expand temporal/trace invariants and implementation-to-model conformance without weakening this evidence boundary.
