# Support and Maturity by Surface

RPOS uses per-surface maturity rather than treating the entire repository as uniformly experimental.

| Surface | Current posture | Notes |
|---|---|---|
| Core Python/SQLite responsibility state machine | Supported | Intended for bounded real integrations within documented state/authority contracts. |
| Persistence / restart / unresolved-effect continuity | Supported | Central runtime behavior with executable regression coverage. |
| Human Gate / denial / explicit resume authority | Supported | Authority transitions are explicit and machine-checkable. |
| Reconciliation / repair / resume paths | Supported | Intended for real bounded recovery flows. |
| Evidence and provenance surfaces | Supported reference | Usable evidence structure; external immutability/signing may require additional systems. |
| Readback/effect-verification patterns | Supported reference | Requires suitable external authoritative readback in the integration. |
| Production-grade local integration demos | Supported examples | Real runtime integration fixtures; not proof of arbitrary production systems. |
| Formal Lean assurance surface | Supported bounded assurance | Machine-checks declared models/invariants, not the whole runtime/deployment. |
| Enterprise deployment authn/authz/tenancy/secrets | Not included | Integrator-owned unless a future scoped surface implements them. |
| Remote production connectors across arbitrary SaaS/legacy systems | Preview / future integration track | Concrete adapters require independent implementation and validation. |
| Universal exactly-once behavior | Unsupported as a universal claim | Only possible where target-side contracts and verification make it defensible. |
| Legal/organizational authority creation | Unsupported | RPOS carries explicit authority state; it does not create legal/institutional authority. |

## Vocabulary

- **Supported** — intended for normal bounded use; defects are accepted and should be repaired.
- **Supported reference** — usable reference surface; some deployment controls remain outside RPOS.
- **Supported example** — executable example demonstrating a tested path, not universal deployment proof.
- **Supported bounded assurance** — assurance is real within the explicitly modeled scope.
- **Preview** — suitable for early integration and feedback; contract may evolve.
- **Not included** — absent from the current product surface.
- **Unsupported** — deliberately not promised or not authority the runtime should create.

`Not guaranteed` does not automatically mean `forbidden`.
