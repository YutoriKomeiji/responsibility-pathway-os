<!--
Document Title: RPOS Security Model and Threat Boundaries
Document Type: Security Model
Status: Pre-public-alpha migration candidate
Header Language: English
Body Language: English
-->

# RPOS Security Model and Threat Boundaries

## Security objective

RPOS protects not only conventional software assets but also the integrity and continuity of responsibility pathways. A security failure may therefore exist even when no secret is stolen: an attacker or faulty component can compromise RPOS if it can make an operation appear authorized, verified, responsibly owned, or complete when the corresponding responsibility conditions were not satisfied.

The security objective for the 0.1.0a1 public-alpha candidate is bounded: prevent or surface high-value responsibility-pathway violations that can be enforced within the current product scope, preserve uncertainty rather than converting it into success, and retain explicit return paths when responsibility-critical dependencies fail.

## Protected responsibility assets

RPOS treats the following as security-relevant integrity assets:

- operation identity and action intent;
- actor, approval authority, execution actor, resume authority, and Residual Owner;
- Human Gate and Human Return Point;
- responsibility state transitions;
- authority freshness, scope, evidence binding, and context binding;
- external-effect verification state;
- evidence identity and supersession lineage;
- event-history continuity;
- idempotency and dispatch-attempt identity;
- release provenance, SBOM, source/artifact hashes, and exported product boundary.

## Primary threat classes

### Authority laundering and replay

An attacker or stale component may attempt to reuse authority for a different actor, operation, action, evidence set, context, or time window. `AuthorityEnvelope` provides an additive fail-closed control for these mismatches. It is not yet mandatory on every existing dispatch path.

### Responsibility-state equivocation

Different system views may claim incompatible states, Residual Owners, Human Return Points, or event histories for one operation. RPOS exposes non-equivocation findings and does not silently select a winner.

### Historical evidence or event substitution

A later evidence item must not silently erase prior evidence identity. Evidence supersession validation requires explicit predecessor links. Responsibility event checkpoints provide deterministic tamper evidence for the complete observed event sequence when the expected checkpoint is retained independently.

### External-effect uncertainty collapse

An execution receipt is not automatically proof that the external effect occurred. Unknown effect remains `EFFECT_UNKNOWN`; recovery and reconciliation do not convert uncertainty into completion by convenience.

### Unsafe degradation

Loss of authority, identity, policy, or effect-verification dependencies is treated as loss of a responsibility precondition. The safe-degradation primitive returns `HOLD`. Supporting dependencies may degrade only with explicit observable status and without creating authority.

### Repair/resume privilege restoration

Repair readiness does not itself restore execution authority. Resume requires the declared resume authority and remains distinct from retry.

### Supply-chain and release substitution

Release-quality evidence includes deterministic export, source-bound hashes, CycloneDX SBOM generation and validation, dependency vulnerability audit, secret scanning, clean installation, and installed-boundary checks. These are point-in-time controls and do not imply permanent absence of vulnerabilities.

## Trust boundaries

The 0.1.0a1 candidate assumes the local Python process, SQLite host, host clock, and independently retained integrity checkpoints are operated within the deployment's trusted computing boundary unless a stronger integration profile is added.

RPOS does not currently claim a trusted hardware root, remote attestation, distributed consensus, universal malicious-operator resistance, or multi-tenant isolation.

External adapters, identity systems, policy systems, MCP/plugin/model integrations, and effect-verification services are separate trust domains. A future integration must define its own identity, credential, input-validation, authority, evidence, timeout, degradation, and failure-return policy before it can inherit strong RPOS security claims.

## Secure-default principles for the alpha

- uncertainty is preserved rather than rounded into success;
- missing responsibility-critical dependency => HOLD;
- invalid state transitions are rejected;
- incorrect approval/resume actors are rejected;
- duplicate dispatch idempotency keys do not redispatch;
- incomplete dispatch after restart moves toward unresolved effect, not blind replay;
- responsibility-history conflicts are surfaced, not auto-resolved;
- superseding evidence preserves predecessor identity;
- public export excludes private research and non-product roots;
- security and release evidence are scoped and time-bounded.

## Explicitly deferred controls

The machine-readable readiness record `provenance/security-quality-readiness-0.1.0a1.json` lists each deferred control with owner, reason, risk, claim impact, and Human Return Point. Material alpha deferrals include cryptographic/hardware-backed integrity anchors, mandatory AuthorityEnvelope enforcement on all legacy dispatch paths, generic MCP/plugin/model trust enforcement, multi-tenant isolation, production DoS/capacity assurance, and scheduled continuous security revalidation.

These deferrals reduce the scope of public claims; they do not convert an unimplemented capability into a promise.
