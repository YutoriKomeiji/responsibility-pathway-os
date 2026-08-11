# RPOS System Architecture v0.1

Status: Private RPP Design / Architecture Candidate

## 1. Purpose

RPOS — Responsibility Pathway Operating System — is an executable responsibility operating layer for governed external operations. It extends the Responsibility Pathway lineage from design and runtime into a process/service that owns operation admission, authority/permission gating, durable responsibility state, dispatch coordination, readback, unresolved-state preservation, recovery, and Human Return.

RPOS is not a general-purpose computer operating system. It is an operating layer for responsibility-bearing operations.

## 2. Architectural rule

```text
Runtime proves existence.
Tests/conformance provide implementation evidence.
Lean proves bounded invariants of the declared normative model.
Operational readback verifies concrete external effects.
No layer substitutes for another.
```

## 3. Reuse from RPR and RPE

Fresh review of RPR and RPE shows reusable concepts already exist:

- RPR has explicit pathway states including approval, running, Human Gate, write-status-unknown, repair-required, ready-to-resume, completed, denied, and aborted.
- RPR binds execution attempts durably and preserves ambiguous write outcomes as unresolved rather than silently redispatching.
- RPR separates execution result from independently verified readback before completion.
- RPR persists actor/authority roles, Human Return Point, residual owner, repair owner, and resume authority in the pathway definition.
- RPE defines a Human Return Point as a designed returnable state, not merely human presence or an approval button.

RPOS will preserve those semantics where they remain valid, but will not silently fork RPR product behavior. RPR reuse must be either an explicit dependency/interface or an explicitly generalized design with provenance.

## 4. Top-level components

```text
                +---------------------------+
                |       Control Plane       |
                | policy / authority / gate |
                +-------------+-------------+
                              |
                              v
+-------------+    +----------+-----------+    +------------------+
| Client/API  +--->+ Operation Supervisor +--->+ Adapter Boundary |
| CLI / MCP   |    | lifecycle / dispatch |    | external effects |
+-------------+    +----+-------------+----+    +--------+---------+
                        |             |                  |
                        v             v                  v
                 +------+-----+ +-----+------+    external systems
                 | State Store | | Evidence   |
                 | durable     | | Ledger     |
                 +------+-----+ +-----+------+
                        |             |
                        +------+------+ 
                               |
                               v
                      +--------+---------+
                      | Recovery Manager |
                      | reconcile/resume |
                      +--------+---------+
                               |
                               v
                      +--------+---------+
                      | Human Return     |
                      | explicit owner   |
                      +------------------+
```

### 4.1 Operation Supervisor
Owns the normative operation lifecycle and is the only component allowed to advance durable operation state.

### 4.2 Control Plane
Resolves policy, declared authority, permission, Human Gate requirements, and admission decisions. Capability never implies permission.

### 4.3 Durable State Store
Persists operation definition, current state, active attempt binding, unresolved obligations, Human Return Point, residual owner, and recovery metadata.

### 4.4 Evidence Ledger
Records structured events with enough provenance to reconstruct why a transition occurred. A log is evidence support, not itself a Return Point or proof of real-world correctness.

### 4.5 Adapter Boundary
Contains bounded external-effect adapters. An adapter returns dispatch/receipt information and, when possible, independent readback. A successful dispatch receipt must not automatically produce VERIFIED or COMPLETED.

### 4.6 Recovery Manager
Handles ambiguous writes, failed execution, reconciliation, repair preparation, restart reconstruction, and resume authorization. It must never redispatch an uncertain operation merely because a process restarted.

### 4.7 Human Return Surface
Produces a compact return package containing state, evidence pointers, unresolved risk, required authority, available actions, residual owner, and next decision point.

### 4.8 Interfaces
Initial product surfaces are CLI and Python API. MCP and remote service/API surfaces follow only after their boundary semantics are explicit and verified.

## 5. Operation lifecycle

Normative high-level lifecycle:

```text
PROPOSED
  -> ADMISSION_PENDING
  -> HUMAN_GATE | AUTHORIZED | DENIED | HELD
  -> DISPATCHING
  -> EFFECT_UNKNOWN | EFFECT_OBSERVED | FAILED
  -> VERIFIED | REPAIR_REQUIRED | UNRESOLVED
  -> COMPLETED | READY_TO_RESUME | HUMAN_RETURN
```

This is an RPOS-level lifecycle and is not asserted to be identical to the current RPR PathwayState enumeration. Detailed design will decide the compatibility mapping.

## 6. Core invariants

Initial invariant families:

- INV-AUTH-001: capability does not imply permission.
- INV-AUTH-002: an operation requiring Human Gate cannot enter dispatch without an accepted human decision from the declared authority path.
- INV-EXEC-001: dispatch receipt does not imply verified external effect.
- INV-EVID-001: VERIFIED requires evidence satisfying the operation's declared verification contract.
- INV-UNK-001: unknown external effect remains unresolved until reconciliation or explicit bounded abandonment/compensation policy resolves it.
- INV-RESP-001: unresolved operation state retains residual owner and Human Return Point.
- INV-RESTART-001: restart reconstruction must not silently create a second dispatch for an unresolved prior attempt.
- INV-CLAIM-001: formal proof scope, implementation evidence scope, and operational evidence scope remain distinct.

## 7. Boot contract

RPOS boot is successful only when:

1. durable store opens and schema is compatible;
2. control-plane configuration is readable;
3. unresolved operations can be enumerated;
4. active/incomplete attempt bindings can be reconstructed;
5. no unresolved attempt is automatically redispatched;
6. health/inspection surfaces become available.

Boot success does not mean all pending operations are safe to continue.

## 8. Restart contract

On restart RPOS reconstructs durable state before accepting new dispatch for an existing operation. Each unresolved attempt is classified into one of:

- safe to continue without redispatch;
- requires reconciliation/readback;
- requires repair;
- requires Human Return;
- terminally denied/aborted/completed.

## 9. Authority and permission model

RPOS separates:

- actor identity declaration;
- authenticated principal/binding where available;
- capability;
- policy applicability;
- declared authority;
- permission;
- Human Gate decision;
- execution actor;
- stop authority;
- repair/resume authority;
- residual owner.

No one field substitutes for another.

## 10. Evidence model

Evidence classes:

- proposal/admission evidence;
- authority/permission evidence;
- dispatch evidence;
- execution receipt;
- independent readback evidence;
- reconciliation evidence;
- repair/resume evidence;
- Human Return package evidence.

Evidence may be cryptographically chained or tamper-evident, but such mechanisms do not by themselves prove truth, legal responsibility, or external immutability.

## 11. Formal verification boundary

Lean 4 models the normative transition system and selected invariants. The executable Python implementation must be mapped by requirement IDs and conformance scenarios.

Lean proof does not by itself prove:

- Python implementation correctness;
- dependency or OS security;
- external adapter truthfulness;
- real-world safety;
- legal responsibility;
- organizational governance quality;
- production readiness.

## 12. Non-goals for early alpha

- general-purpose OS kernel;
- identity provider or credential vault;
- legal-responsibility adjudicator;
- universal policy language;
- exactly-once guarantee over arbitrary remote systems;
- production gateway claim;
- blanket formally verified product claim;
- autonomous replacement of responsible human/institutional authority.

## 13. First executable slice

The first vertical slice will implement:

1. bootable `RposService` process object;
2. SQLite durable store;
3. operation proposal with actor / authority / Human Return metadata;
4. admission into AUTHORIZED or HUMAN_GATE;
5. explicit human approval transition;
6. one bounded in-memory/test adapter;
7. dispatch with attempt ID and idempotency key;
8. receipt/readback separation;
9. unresolved effect state;
10. restart reconstruction and inspection;
11. CLI smoke surface later in the same subsystem.

This slice is intentionally small enough for fast focused verification while proving the architectural path is executable.
