# Japan-first Cyber / Software Supply-chain Evidence Boundary v0.1

## Status

Private alpha engineering profile. This document is a bounded RPOS engineering mapping, not a legal interpretation, certification profile, or statement of conformity.

## Official Japanese source context

Primary reference: Ministry of Economy, Trade and Industry, `サイバーインフラ事業者に求められる役割等に関するガイドライン`, published 2026-03-31, together with its evaluation checklist materials.

The official material addresses software development, supply, and operation; customer/provider responsibility; software supply-chain cyber resilience; and evidence-oriented evaluation records.

RPOS does not claim that the fields below exhaust, implement, or satisfy that guidance.

## RPOS engineering interpretation

RPOS needs a bounded evidence class for dependencies used by an operation so that responsibility history can answer, without promoting state:

- which component, adapter, or external service was relied on;
- which source reference and source revision were observed;
- which component version was recorded;
- which dependency owner remains responsible for review;
- which verification method was used;
- whether an artifact digest was recorded;
- which supplier role was declared, when applicable;
- which unresolved dependency risk remains.

## Evidence model

`DependencyEvidence` is intentionally separate from:

- authority and admission evidence;
- external evaluation evidence;
- dispatch and receipt evidence;
- external-effect readback evidence;
- repair and resume evidence.

Allowed evidence classes in v0.1:

- `software_component`
- `adapter`
- `external_service`

Strict serialized import requires:

- `evidence_id`
- `evidence_class`
- `source_system`
- `source_reference`
- `source_revision`
- `component_name`
- `component_version`
- `dependency_owner`
- `verification_method`

Optional bounded fields:

- `artifact_digest`
- `supplier_role`
- `unresolved_risk`

Unexpected fields are rejected. This prevents a nominal dependency-evidence channel from becoming an unbounded path for credentials, environment dumps, raw logs, prompts, or unrelated payloads.

## State boundary

Recording dependency evidence MUST NOT:

- authorize an operation;
- satisfy a Human Gate;
- start dispatch;
- establish operational `VERIFIED`;
- complete an operation;
- establish supplier trust;
- prove software supply-chain conformity.

The event `dependency_evidence_recorded` is evidence-only and produces no responsibility-state transition.

## Audit boundary

`rpos.audit.v0.1` exposes dependency evidence under the separate group `dependency_supply_chain`.

The audit package explicitly retains at least these non-claims:

- `supplier_or_dependency_trustworthiness`
- `software_supply_chain_conformance`
- `legal_or_regulatory_compliance`

## Follow-on work

1. Add a partial Japan cyber-guideline evidence matrix with `evidence_present` / `gap` only.
2. Map Dependency Owner, adapter evidence, external-effect verification, recovery/resume, and unresolved responsibility to bounded source expectations.
3. Keep all official-source statements distinct from RPOS engineering interpretation.
4. Do not emit `compliant`, certification, endorsement, or legal-conformity conclusions.
