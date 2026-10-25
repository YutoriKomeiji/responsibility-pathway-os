# RPR → RPOS Responsibility Routing semantic crosswalk (candidate)

Status: unreleased source candidate; semantic mapping only, **not a runtime integration adapter**.

RPR `src/rpr/models.py` defines `ResponsibilityRouteClass` and a route envelope with receiver eligibility, authority class, delegation scope, unresolved payload, allowed actions, reevaluation and closure conditions, residual owner and optional expiry. RPOS currently defines a different operation-state-driven routing classifier and a separate, opt-in eligibility assessment helper.

`rpos.rpr_route_crosswalk.crosswalk_rpr_route_class` deliberately returns a *bounded semantic mapping*:

| RPR route class | RPOS mapping | Reason |
|---|---|---|
| `hold_for_reconciliation` | `HOLD_FOR_RECONCILIATION` (semantic only) | Both distinguish ambiguous effects from human escalation |
| `bounded_human_return` | Requires contextual review | RPOS `HUMAN_GATE` requires an actual approval state and appropriately eligible authority, not just an RPR route label |
| `continue_autonomously` | Requires contextual review | RPOS has no equivalent unresolved-operation route |
| `ai_resolve_within_delegation` | Requires contextual review | Delegation and host authorization must be checked, not inferred |
| `stop_and_preserve_residue` | Requires contextual review | RPOS terminal/hold states and residual ownership need state-aware evaluation |

**Critical boundary:** Even the reconciliation mapping is a vocabulary equivalence, not evidence that a recipient is eligible or that a persisted operation may transition. Caller must still inspect actual RPOS state, independent host authorization, delegation, recipient eligibility, evidence access, timeout/expiry and residual owner. No method in this crosswalk may dispatch, select a receiver, revive permission after restart or grant Authority.

This table is tested against a pinned RPR source vocabulary as manually inspected on 2026-10-25. It is **not** an automated live compatibility matrix and must be re-reviewed when RPR enums change. RPR is not added as a runtime dependency. Subsequent work may introduce a versioned envelope and executable integration scenarios after owner-level source/compatibility review.

See `src/rpos/rpr_route_crosswalk.py` and `tests/test_rpr_route_crosswalk.py`.
