<!--
Document Title: RPOS OS-Quality Readiness
Document Type: Product Quality Readiness Note
Status: Pre-public-alpha migration candidate
Header Language: English
Body Language: English
-->

# RPOS OS-Quality Readiness

## Scope

RPOS uses "Operating System" to describe an operating layer for responsibility state, authority, external-effect verification, reconciliation, repair, resume, evidence, and Human Return Points. The 0.1.0a1 alpha is therefore evaluated as a software product with operating-layer quality obligations, not as a conventional kernel or general-purpose host OS.

This note summarizes the quality attributes that are implemented and verified enough for repository migration, while keeping production-readiness claims explicitly out of scope.

## Functional suitability

The executable core supports proposal, Human Gate, authorization, dispatch, effect verification, effect-unknown containment, reconciliation, repair preparation, explicit resume authorization, completion, persistent state, CLI/examples, and evidence/provenance helpers.

Invalid transitions and wrong approval/resume actors are rejected. Receipt success does not substitute for required effect verification.

## Reliability and recoverability

Incomplete dispatch detected after restart is recovered to unresolved external-effect handling without automatic redispatch. Idempotency keys prevent duplicate redispatch for a previously recorded attempt. Repair readiness remains separate from restored authority.

The alpha does not claim arbitrary-operation liveness, distributed failover, or production availability SLOs.

## Compatibility

Security hardening through the current candidate is additive and classified `backward_compatible`. Existing supported alpha persisted records remain readable through compatibility defaults. A future change that makes new security envelopes mandatory must receive a separate compatibility classification.

## Operability and diagnosability

RPOS exposes explicit states, Human Return Packages, unresolved reasons, event history, reconciliation evidence, security-degradation reasons, and responsibility-integrity findings. Failure states are intended to remain inspectable rather than collapse into generic success/failure.

Sensitive-data minimization remains deployment/integration dependent; operators must not treat the event store as a safe place for arbitrary secrets.

## Maintainability and testability

The product separates models, storage, service orchestration, adapters, evidence, provenance, security primitives, templates, CLI, tests, examples, and bounded Lean artifacts. Public claims are cross-walked to implementation, tests, assumptions, and Not Proven boundaries.

## Portability and installability

Release verification builds wheel and source distribution, performs isolated installation, exercises the installed CLI and Quick Start outside the repository working directory, and validates the deterministic public-export boundary.

## Supply-chain and release integrity

The release-quality workflow generates and schema-validates a CycloneDX SBOM, audits declared Python dependencies, scans the standalone source export for likely secrets, creates source-bound artifact hashes, and retains release-quality evidence.

These checks are point-in-time evidence. They do not imply certification or permanent absence of vulnerabilities.

## Responsibility-specific quality properties

RPOS additionally treats the following as product-quality properties:

- uncertainty preservation;
- responsibility continuity under partial failure;
- explicit Residual Owner / Human Return Point retention;
- authority freshness and context binding primitives;
- responsibility-state non-equivocation detection;
- tamper-evident responsibility-event checkpoints;
- evidence supersession without silent erasure;
- fail-closed degradation of authority/identity/policy/effect-verification dependencies.

## Deferred quality attributes

The machine-readable readiness record lists explicit alpha deferrals. Major remaining areas are production workload/capacity objectives, multi-tenant isolation, generic integration trust enforcement, cryptographic external integrity anchors, mandatory use of newer security primitives on all legacy paths, and recurring post-release security revalidation.

Each deferral has an owner, risk, claim impact, and Human Return Point. These are not hidden gaps and do not authorize stronger production claims.

## Migration-readiness rule

Repository migration may proceed only after the exact candidate head passes focused Python verification, public-export RC verification, JA/EN documentation sync, and release-quality evidence checks. Green verification authorizes evidence retention for migration readiness; it does not by itself authorize repository public visibility, tag/release, PyPI publication, Pages/demo, or external announcement.
