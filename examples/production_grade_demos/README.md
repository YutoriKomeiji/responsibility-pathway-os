# Production-Grade Operational Demos

> Executable integration scenarios for RPOS `0.1.0a2`.
>
> These demos do not reimplement the RPOS state machine. They invoke the shipped `RposService`, use its SQLite persistence and transition rules, and communicate with a separate localhost HTTP service backed by its own SQLite database.

## Why this is not a success-only mock walkthrough

The demo harness starts a real HTTP process on localhost and persists external effects outside the RPOS database. RPOS communicates with that process through an adapter using normal HTTP requests. Independent reconciliation uses a separate GET readback path.

The external service is a deterministic integration fixture, not a production payment processor, deployment controller, or IAM system. Its purpose is to make destructive or consequential behavior reproducible without real credentials or third-party systems. The RPOS runtime, Human Gate transitions, dispatch state, failure containment, persistence, process restart, repair/resume, reconciliation, and retained event evidence are product code.

## Scenarios

### 1. Supplier payment — accepted remotely, connection lost

Business risk: a supplier payment may have been accepted even though the caller never received a response. Blind retry could pay twice.

The demo:

1. proposes a supplier payment;
2. requires explicit `finance_approver` approval;
3. sends the payment to the localhost payment endpoint;
4. the external service commits the effect and then deliberately drops the connection;
5. RPOS records `effect_unknown` instead of success or safe retry;
6. the RPOS worker process exits;
7. a new Python process opens the same RPOS SQLite database;
8. independent HTTP readback finds the committed payment;
9. RPOS completes from reconciliation evidence;
10. the external database proves `apply_count == 1`.

This is the central demonstration that a transport failure after a real external write is not equivalent to a failed write.

### 2. Production deployment — rejection, repair, reauthorization, completion

Business risk: a production rollout may be rejected by an external deployment controller and must not silently bypass the rejected state.

The demo:

1. proposes a production release promotion;
2. requires `change_manager` approval;
3. the deployment controller rejects the first dispatch;
4. RPOS enters `repair_required`;
5. operations records repair preparation;
6. the `change_manager` explicitly resumes the pathway;
7. a second dispatch is accepted;
8. receipt remains distinct from effect verification;
9. independent readback confirms the deployment;
10. RPOS reaches `completed` with one external application.

### 3. Privileged access revocation — Human Gate denial

Business risk: an automated security recommendation may be plausible but still premature while identity investigation is incomplete.

The demo:

1. proposes privileged-access revocation;
2. returns to `security_duty_manager` Human Gate;
3. the authority denies execution;
4. RPOS records `denied`;
5. the external service database proves no access-side effect occurred.

This demonstrates that a model or automation proposal is not execution authority.

## Run

From an installed or repository environment with RPOS available:

```bash
python examples/production_grade_demos/run_demo.py
```

The command produces deterministic JSON and exits non-zero if any responsibility invariant exercised by the scenarios is violated.

To retain SQLite files for inspection:

```bash
python examples/production_grade_demos/run_demo.py --workdir ./demo-state
```

The retained directory contains separate RPOS databases and the external-system database.

## Acceptance criteria

The suite is acceptable only when automated verification demonstrates all of the following:

- the scripts use the shipped RPOS package rather than a copied state machine;
- external effects occur through localhost HTTP into a separate SQLite store;
- the supplier-payment transport ambiguity results in `effect_unknown`;
- the unresolved payment survives a real Python process restart;
- authoritative readback completes the payment without redispatch;
- payment `apply_count` remains exactly one;
- production deployment rejection enters `repair_required`;
- repair requires explicit resume by the declared authority;
- accepted deployment remains non-complete until readback;
- deployment applies exactly once;
- Human Gate denial creates zero privileged-access external effects;
- no real credentials, customer data, third-party endpoint, or production system is contacted.

## Claim boundary

Passing these demos verifies these declared scenarios in the tested environment. It does not establish production readiness, financial or security compliance, authenticated human identity, credential protection, arbitrary external exactly-once delivery, or correctness of a real payment/deployment/IAM provider.

A production deployment must provide domain-specific authorization, identity assurance, credential isolation, network policy, provider contracts, independent readback semantics, incident procedures, and operational ownership.
