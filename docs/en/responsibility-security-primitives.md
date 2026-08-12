<!--
Document Title: RPOS Responsibility Security Primitives
Document Type: Security Design Note
Status: Pre-public-alpha candidate
Header Language: English
Body Language: English
-->

# RPOS Responsibility Security Primitives

## Scope

This note defines the first RPOS-native security primitives added under the 2026-08-12 security hardening track. They complement, rather than replace, established software and AI security controls.

The design is informed by current official/public guidance including NIST's AI-agent security work, OWASP AISVS 1.0, the OWASP Top 10 for Agentic Applications 2026, CISA Secure by Design guidance, and the product-quality framing of ISO/IEC 25010:2023. Mapping a control to these sources does **not** imply certification, conformity, endorsement, or complete coverage.

## Why RPOS needs responsibility-specific security

Traditional security protects confidentiality, integrity, availability, identity, authorization, software supply chains, and operational boundaries. RPOS must protect those properties too. In addition, a responsibility-pathway system can be compromised even when no secret is stolen if an attacker or faulty component can make an operation appear responsibly authorized or completed when it was not.

Examples include:

- replaying stale approval for a different operation;
- reusing authority after the evidence or operating context changed;
- making two system views disagree about the current responsibility state;
- replacing a Residual Owner or Human Return Point without detection;
- presenting a shorter or different event history as authoritative;
- converting unresolved external effect into completion by convenience.

The first implementation slices therefore treat responsibility metadata, responsibility-state agreement, and responsibility-history integrity as protected domains.

## Primitive 1: Authority Freshness Envelope

`AuthorityEnvelope` binds authority evidence to:

- actor;
- operation id;
- action name;
- issue time;
- expiry time;
- evidence digest;
- context digest.

`validate_authority_envelope()` is fail-closed. A stale, future-dated, actor-mismatched, operation-replayed, action-replayed, evidence-mismatched, or context-mismatched envelope returns `HOLD` with explicit reasons.

This is an **additive primitive** in the current slice. Existing RPOS state authorization remains authoritative unless a caller explicitly adopts envelope validation. Making an envelope mandatory on every dispatch would be a behavior change and requires compatibility review before enforcement.

## Primitive 2: Responsibility Integrity Snapshot

`ResponsibilityIntegritySnapshot` creates a canonical SHA-256 digest over a responsibility-critical projection:

- operation id;
- state;
- Residual Owner;
- Human Return Point;
- event count;
- latest event digest.

The purpose is tamper sensitivity and cross-view comparison. It is not a digital signature, trusted timestamp, or proof that the underlying event content is true.

## Primitive 3: Responsibility-State Non-Equivocation Monitor

`find_responsibility_inconsistencies()` compares responsibility snapshots for the same operation and reports disagreements instead of selecting a winner.

Current findings include conflicts in:

- responsibility state;
- Residual Owner;
- Human Return Point;
- event-history length;
- latest-event digest.

A caller can use these findings to HOLD execution or route the operation to responsible review. Automatic conflict resolution is deliberately outside this primitive.

## Primitive 4: Responsibility Event-Chain Checkpoint

`build_event_chain_checkpoint()` computes a deterministic SHA-256 hash chain over the complete observed event sequence for one operation. `RposService.event_chain_checkpoint()` exposes that checkpoint over the actual stored event history.

The builder rejects cross-operation event substitution and non-monotonic sequence order. If a previously retained checkpoint is compared with a later history after an old event has been modified, the chain digest changes and `event_chain_matches()` returns false.

This adds a practical **tamper-evidence primitive** without changing the SQLite schema. The expected checkpoint must be retained independently from the mutable event store to provide meaningful detection. A checkpoint stored only beside the same compromised database would not create an independent trust anchor.

## Security properties tested in the current slices

The current negative/integration tests establish that:

1. expired authority fails closed;
2. an authority envelope replayed for another operation fails closed;
3. authority is bound to the evidence and context digests supplied by the caller;
4. responsibility-integrity digests are deterministic and change when protected fields change;
5. conflicting responsibility views are surfaced rather than silently collapsed;
6. the monitor does not invent a conflict when equivalent views agree;
7. unchanged event history produces a stable event-chain checkpoint;
8. appending a valid event advances the checkpoint;
9. mutation of a historical event invalidates a previously retained checkpoint;
10. cross-operation event substitution and non-monotonic event ordering are rejected.

## Relationship to public standards and current agent-security work

As of 2026-08-12:

- NIST's 2026 AI-agent security work reports broad agreement that existing cybersecurity principles remain relevant but require adaptation for AI agents, and NIST's AI Agent Standards Initiative includes identity, authorization, secure interactions, and security evaluation as active work areas.
- OWASP AISVS 1.0 (released 2026-06-24) defines testable AI-security requirements across access control and identity, supply chain, memory, autonomous/agentic action, MCP, adversarial robustness, and monitoring/logging.
- OWASP's Top 10 for Agentic Applications 2026 identifies risks specific to systems that plan and act across workflows.
- CISA Secure by Design guidance places responsibility on software manufacturers to make secure behavior a product property rather than shifting all hardening burden to customers.
- ISO/IEC 25010:2023 provides a nine-characteristic product-quality model usable for requirements, test objectives, quality control, and acceptance criteria.

RPOS uses these as evidence inputs for the broader #201/#202 hardening program while retaining a separate RPOS-native responsibility-security layer.

## Current limitations and extension path

The current slices do not yet claim:

- mandatory envelope enforcement on every dispatch;
- cryptographic signatures or hardware-backed keys;
- distributed consensus between independent replicas;
- trusted time or protection from compromised host clocks;
- an immutable or externally anchored event ledger;
- automatic safe conflict resolution;
- proof that SQLite or the Python runtime conforms to the bounded Lean model;
- immunity to prompt injection, compromised plugins/MCP servers, malicious operators, or supply-chain compromise.

These are current-scope boundaries, not declarations that the capabilities cannot be added. Follow-on security work will evaluate mandatory enforcement, evidence supersession chains, external checkpoint anchoring, degradation policy, integration trust, secret isolation, persistence tamper detection, security telemetry, and continuous revalidation.

## Compatibility classification

These slices are `backward_compatible`: they add security APIs and tests without changing the existing persisted schema or requiring existing callers to provide authority envelopes or event checkpoints.

A later move from optional validation to mandatory dispatch enforcement, or from externally retained checkpoints to a new persisted integrity schema, must be classified separately and may require `compatibility_adapter_required` or `breaking_change_human_gate` treatment.
