# Claim Boundary Promotion

RPOS treats public claims as evidence-governed states, not as permanent disclaimers.

A current non-claim can mean one of two different things:

1. an **evidence-limited boundary** that can move when declared evidence is obtained and reviewed; or
2. a **permanent responsibility boundary** that RPOS should not cross by itself, regardless of maturity.

These two cases must not be presented as if they were the same.

## Current evidence boundary

RPOS 0.1.0a1 is an Early Public Alpha / Executable Preview. Its verified surface includes bounded executable Python behavior, persistence and recovery scenarios, clean package installation, public-export reconstruction, SBOM and source-bound checks, selected Windows portability evidence, and a bounded Lean model for explicitly stated abstract properties.

That evidence supports the current Public Alpha claims only. It does not automatically support production, legal, organizational, external-system, or implementation-wide formal claims.

## Promotion criteria

The following boundaries are evidence-limited and may move after reviewable evidence is added.

| Current boundary | Evidence that can move the boundary |
|---|---|
| No production-readiness claim | sustained workload and soak tests; fault injection across supported deployment profiles; upgrade, rollback, backup and recovery evidence; operational monitoring/SLO evidence; reviewed security and deployment controls |
| Limited platform/field evidence | a declared support matrix with reproducible CI and field results across supported OS, Python, container, network, identity and storage profiles |
| No implementation-wide formal-conformance claim | an explicit refinement/conformance relation between the formal model and executable semantics, plus independently reproducible conformance evidence for the claimed implementation surface |
| No broad software-supply-chain trust claim | stronger dependency provenance, immutable CI inputs where justified, artifact signing/attestation, independent verification and maintained vulnerability-response evidence |
| No bounded-domain effectiveness claim beyond current scenarios | domain-specific pilots with declared hypotheses, failure criteria, observed outcomes, counterexamples and independent review |

Promotion is not automatic. New evidence must be scoped, reviewable, reproducible where applicable, and explicitly admitted into the corresponding public claim.

## Permanent responsibility boundaries

The following are not expected to disappear merely because RPOS matures:

- RPOS does not create legal authority, legal interpretation, legal liability, certification, or regulatory approval by itself.
- RPOS does not make an external system correct merely because it governs the pathway to that system.
- RPOS does not turn a transport receipt into proof of a real-world effect without an appropriate verification contract and evidence source.
- RPOS does not transfer final organizational responsibility from the responsible human or institution to the software.
- RPOS cannot provide a universal exactly-once guarantee for arbitrary external systems that do not expose the necessary transactional/idempotency/verification contract.
- RPOS does not make a formal proof about an abstract model automatically prove the complete Python implementation or deployment environment.

These are responsibility boundaries, not unfinished features.

## Evidence owners

- **RPOS engineering** owns executable state-machine, persistence, recovery, packaging and declared implementation evidence.
- **Integrators/operators** own deployment-specific identity, credentials, network controls, bypass prevention, monitoring and authoritative external-effect observation.
- **RPE/RPD/RPM and assurance work** may supply upstream requirements, engineering obligations, design rationale, review structures and theory revision; evidence from one layer must not impersonate evidence from another.
- **Qualified human/institutional authorities** own legal, regulatory, certification and operational-authorization decisions.

## Promotion states

When a public boundary is tracked explicitly, use one of these states where practical:

- `evidence_collecting`
- `review_ready`
- `promoted`
- `permanently_out_of_scope`

A public non-claim should therefore say whether it is a temporary evidence gap or a permanent responsibility boundary. Temporary gaps should expose what evidence would be needed to move them.
