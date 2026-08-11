<!-- RPOS-DOC-ID: RPOS-CLAIM-XWALK-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../ja/public-claim-evidence-crosswalk.md -->

# RPOS Public Claim / Evidence Crosswalk

Status: reviewable claim ceiling for the public alpha candidate.

RPOS may use strong technical terms when the public artifact and evidence support the stated scope. This crosswalk defines the evidence required for those terms and the stronger paraphrases that remain out of scope.

| Term / public claim | Intended bounded wording | Implementation evidence | Test/example evidence | Formal evidence | Not proven / unacceptable stronger paraphrase |
|---|---|---|---|---|---|
| Responsibility Pathway Operating System | executable responsibility operating layer for consequential AI/automation workflows | `src/rpos/`, durable state, CLI, reconciliation/repair/resume surfaces | focused tests; four primary source examples | bounded state/evidence invariants | not a general-purpose OS; not governance-completed; not production certification |
| runtime | executable Python runtime/service layer with durable responsibility state | package under `src/rpos/` | wheel/install/CLI tests and examples | no whole-runtime proof | not proof that every adapter/external system is correct |
| formally modeled | selected responsibility states, transitions, evidence classes, and packet authority boundaries are expressed in Lean 4 | `formal/lean/*.lean` | Lean CI compilation | direct theorem sources | does not mean the Python implementation is formally modeled in full |
| formally verified | only when naming the exact theorem/property accepted by Lean | theorem-specific | Lean workflow | theorem-specific | do not say `RPOS is fully formally verified` |
| verified | use only with the object and verifier named, e.g. `verified external effect` after configured readback/reconciliation | verification/reconciliation implementation | happy path and restart/reconciliation examples/tests | separation between receipt and effect evidence | receipt, dispatch success, or local return value alone is not verified external effect |
| assurance | bounded evidence/authority/effect boundaries that support review and safe incompletion | responsibility state/evidence surfaces | focused tests/examples | evidence-separation invariants | no universal assurance, safety certification, or compliance guarantee |
| security | security boundary/documentation and fail-closed validation where implemented | validators, credential boundaries, bounded adapter design | relevant validation/security tests | no deployment-security theorem | not a claim that arbitrary deployments are secure |
| evidence | typed/source-tagged artifacts used for authorization, evaluation, dependency, verification, provenance, or review | evidence models and reports | evidence-specific tests | evidence-class separation | evidence possession does not automatically grant authority or prove truth/completeness |
| external-effect verification | independent observation/readback sufficient for the configured operation contract | reconciliation/readback path | restart/reconciliation example/tests | receipt != effect-verification theorem | no claim of exactly-once or universally trustworthy readback |
| reconciliation | explicit process for resolving an uncertain external effect from later evidence/readback | reconciliation service/runtime path | `effect_unknown_restart_reconcile.py` and tests | modeled path from uncertainty to verification/repair | no guarantee every uncertainty can be resolved |
| repair | bounded preparation after failure/uncertainty that may establish readiness to request resumption | repair state/API | repair/resume scenario/tests | `REPAIR_REQUIRED -> READY_TO_RESUME` boundary | repair does not restore execution authority |
| resume | explicit authority-restoration step producing authorization for a fresh attempt | resume API/state transition | repair -> ready -> resume -> fresh attempt scenario/tests | ready-to-resume -> authorized; no direct dispatch | resume is not retry and does not itself prove external effect |
| Human Gate | explicit human decision boundary for configured consequential actions | gate/admission surfaces | denial/no-dispatch scenario/tests | Human Gate cannot directly dispatch | not a transfer of legal/organizational responsibility to software |
| responsibility packet/template | machine-readable role/evidence/decision handoff structure | `template_packets.py`, `templates/` | `test_template_packets.py` | packet authority boundary | packets/templates cannot create authority or state transitions |

## Claim construction rule

A public statement should be reconstructable as:

`claim -> implementation artifact -> executable evidence -> formal evidence where applicable -> assumptions -> not_proven`.

When one link is absent, the public wording must not imply that the missing evidence class exists.

## Search / AI-summary resilience

Authoritative terminology is allowed and useful when accurate. To reduce over-broad search-engine or LLM paraphrases, release-facing pages should keep the scoped object close to the strong term, for example:

- `Lean 4 machine-checked bounded state-transition invariants` rather than `formally verified system`;
- `external effect verified by configured readback` rather than `execution verified`;
- `executable responsibility operating layer` together with the explicit alpha / Not Proven boundary.
