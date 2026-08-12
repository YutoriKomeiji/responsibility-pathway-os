<!--
Document Title: RPOS Evidence Supersession and Safe Degradation
Document Type: Security Design Note
Status: Pre-public-alpha candidate
Header Language: English
Body Language: English
-->

# RPOS Evidence Supersession and Safe Degradation

## Purpose

This note defines two additive responsibility-security controls for RPOS: explicit evidence supersession lineage and fail-closed degradation of responsibility-critical dependencies.

These controls complement the Authority Freshness Envelope, responsibility-integrity snapshots, non-equivocation checks, and event-chain checkpoints already implemented in RPOS. They do not replace conventional identity, access-control, network, host, supply-chain, or AI-agent security controls.

## Evidence Supersession Chain

A later evidence item may legitimately replace an earlier conclusion. RPOS must nevertheless preserve the fact that the earlier evidence existed and identify which evidence superseded it.

`EvidenceSupersessionRecord` retains:

- evidence id;
- evidence digest;
- source reference;
- predecessor evidence id, when superseding;
- reason for supersession, when supplied.

`validate_evidence_supersession_chain()` treats the first record as the retained root. Every later record must point explicitly to the immediately preceding evidence id. Duplicate identities, self-supersession, broken predecessor links, and replacement without a supersession link are rejected.

The purpose is anti-substitution provenance. It does not prove that the evidence itself is true, trustworthy, or correctly interpreted.

## Safe Degradation of Responsibility Functions

RPOS distinguishes responsibility-critical dependencies from supporting dependencies.

Current dependency criticality classes are:

- authority;
- identity;
- policy;
- external-effect verification;
- supporting.

A responsibility-critical dependency that is degraded or unavailable causes `evaluate_responsibility_degradation()` to return `HOLD`. The caller must not infer or inherit missing authority merely because another service is available.

A supporting dependency may degrade or become unavailable while the decision remains `ALLOW`, but that degradation is returned explicitly in the decision for operator visibility and telemetry.

This is intentionally stricter than a generic "best effort" fallback. Loss of an authority-, identity-, policy-, or effect-verification-critical dependency is treated as loss of a responsibility precondition.

## Security properties covered by tests

The current tests verify that:

1. explicit linear evidence supersession is accepted;
2. silent evidence replacement is rejected;
3. broken predecessor links are rejected;
4. duplicate evidence identities are rejected;
5. degraded authority dependencies fail closed;
6. unavailable effect-verification dependencies fail closed;
7. supporting-service degradation remains observable without inventing authority;
8. availability of a supporting dependency cannot override a critical dependency failure.

## Compatibility

This slice is `backward_compatible`. It adds APIs and tests without changing the persisted RPOS schema or requiring existing dispatch callers to provide degradation status or evidence-supersession records.

Mandatory enforcement inside all dispatch/reconcile/resume paths is a later compatibility and security decision.

## Current scope and extension path

This slice does not yet claim cryptographic evidence signing, trusted timestamps, remote attestation, distributed consensus, automatic policy discovery, or universal safe degradation.

Follow-on work may connect these primitives to:

- external integrity anchors;
- responsibility-security telemetry;
- MCP/plugin/integration trust policies;
- continuous security revalidation;
- bounded dispatch enforcement;
- signed or hardware-backed evidence where justified.

These are extension paths, not commitments or claims of present support.
