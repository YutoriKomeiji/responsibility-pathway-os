<!-- RPOS-DOC-ID: RPOS-FORMAL-XWALK-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../ja/formal-evidence-crosswalk.md -->

# RPOS Formal Evidence Crosswalk

Status: bounded formal-evidence mapping for the public alpha candidate.

This document connects public RPOS responsibility rules to Lean 4 artifacts and executable implementation evidence. It does not claim whole-system conformance between the Lean model and the Python runtime.

| Responsibility rule | Lean evidence | Executable evidence | Assumption / boundary | Not proven |
|---|---|---|---|---|
| only authorized work may directly enter dispatch | `RPOS.only_authorized_enters_dispatching` | `examples/happy_path_verified.py`; focused runtime tests | Lean `Step` is the bounded normative transition relation | Python/Lean whole-system conformance |
| Human Gate cannot dispatch directly | `RPOS.human_gate_cannot_dispatch_directly` | `examples/human_gate_denied.py` | Human Gate behavior is modeled only through declared states/transitions | correctness of arbitrary external approval systems |
| completion requires verified state | `RPOS.only_verified_enters_completed` | happy-path and reconciliation scenarios | `VERIFIED` is the bounded RPOS state, not a universal truth predicate | truth/completeness of arbitrary external evidence |
| execution receipt is not external-effect verification | `RPOS.receipt_not_effect_verification` | `examples/effect_unknown_restart_reconcile.py`; reconciliation tests | evidence classes are intentionally bounded | correctness of arbitrary readback sources |
| `EFFECT_UNKNOWN` cannot directly complete | `RPOS.effect_unknown_cannot_complete_directly`; `RPOS.effect_unknown_is_not_completed` | restart/reconciliation scenario | positive completion path is an existence witness only | liveness/eventual completion |
| repair readiness does not restore execution authority by itself | `RPOS.ready_to_resume_is_not_authorized`; `RPOS.repair_required_cannot_authorize_directly` | repair/resume scenario in Quick Start/tests | state separation models authority restoration explicitly | organizational legitimacy of the human authority |
| resume restores authority before any fresh dispatch | `RPOS.ready_to_resume_restores_authority`; `RPOS.resume_does_not_dispatch_directly` | repair -> ready -> resume -> fresh attempt scenario | resume path is bounded to the declared transition model | arbitrary retry semantics outside RPOS |
| reusable responsibility packets cannot grant authority | `RPOS.valid_reusable_packet_cannot_grant_authority`; `RPOS.valid_reusable_packet_has_no_authority_effect` | `src/rpos/template_packets.py`; `tests/test_template_packets.py` | Lean packet model mirrors the public `authority_effect = none` contract | formal proof of Python parser/validator conformance |
| safety/capability/dependency evidence cannot substitute for authorization | `RPOS.safety_evaluation_not_authorization_relevant`; `RPOS.capability_evaluation_not_authorization_relevant`; `RPOS.dependency_evidence_not_authorization_relevant` | evaluation/dependency evidence tests | evidence relevance classes are abstract, not a complete ontology | adequacy of every external evaluator or dependency source |
| positive reachability is not liveness | comments and theorem scope in `RPOSReachability.lean` | recovery examples demonstrate paths, not guarantees | `Steps` proves existence of modeled paths | eventual completion for arbitrary operations |

## Evidence classes

RPOS keeps these evidence classes separate:

1. Lean proof evidence over the declared abstract model.
2. Executable Python implementation/test evidence.
3. Operational external-effect observation/readback evidence.

A result from one class must not be presented as proof from another class.

## Public wording boundary

Acceptable wording must identify the scope, for example: `Lean 4 machine-checks bounded RPOS state/evidence invariants.`

Unacceptable stronger wording includes: `RPOS is fully formally verified`, `Lean proves the Python runtime correct`, or `formal verification proves production safety/compliance`.
