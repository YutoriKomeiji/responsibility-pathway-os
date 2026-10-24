# Route receiver eligibility — opt-in assessment (source candidate)

This experimental helper makes a missing or ineligible recipient **explicit** instead of silently interpreting a named recipient or Human Return destination as permission to transfer work. It does not change the existing published `classify_responsibility_route()` result or serialized operation state.

```python
from rpos.route_eligibility import assess_route_receiver

assessment = assess_route_receiver(
    proposed_route,
    authority_verified=True,
    delegation_verified=True,
    evidence_access_verified=True,
    intervention_capacity_verified=True,
    timing_verified=True,
    eligibility_basis="external host check reference",
    residual_owner="operator",
)
if assessment.permitted_to_transfer:
    # The host still needs its own authorization for any consequential action.
    ...
else:
    # Keep the operation held with its original residual owner.
    ...
```

**Meaning of inputs:** Each `*_verified` fact is **supplied by the integrator**; this function cannot independently verify credentials, delegation, identity, access, capacity, or deadlines. A Boolean `True` without genuine host-side evidence is not security validation. A nonempty `eligibility_basis` is a provenance label supplied by caller, not a verified certificate. Do not use the helper as a security authorization decision by itself.

Three-state result: explicit false → `ineligible`; all independently verified true plus receiver and basis → `eligible`; otherwise → `unknown`. Both ineligible and unknown propose `neutral_hold` and set `permitted_to_transfer=False` rather than default to Human Return. Original route and responsibility owner are preserved in the result. Eligibility to receive information or a route is **not** execution or resume Authority.

**Scope limits:** This first increment is an in-memory assessment for integration and negative tests, not a persisted, restart-safe route envelope. The next stage must decide schema, evidence references, re-evaluation on expiry and persistence compatibility before changing runtime route dispatch or claiming durable receiver-eligibility enforcement. No new public release or general formal-proof claim is implied.
