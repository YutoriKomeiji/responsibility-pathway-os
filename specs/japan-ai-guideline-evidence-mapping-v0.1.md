# RPOS Japan AI Guideline Evidence Mapping v0.1

Status: Private RPP Engineering Profile / Japan-first / Partial Mapping

## Purpose

Map selected engineering expectations from Japan's AI Guidelines for Business Ver.1.2 to concrete RPOS mechanisms, available evidence groups, explicit gaps, and Not-Proven boundaries.

This is not a compliance checklist, legal interpretation, official conformity assessment, or endorsement by any public authority.

## Source profile

Reference profile: AI Guidelines for Business Ver.1.2, published 2026-03-31.

The v0.1 RPOS profile is intentionally partial. It begins with engineering areas already connected to executable RPOS mechanisms and evidence rather than attempting to encode the full official checklist prematurely.

## Machine-readable output

```text
rpos --db <database> guideline-matrix <operation_id>
```

Schema: `rpos.guideline-matrix.v0.1`.

Each row contains:

- internal mapping id;
- bounded engineering expectation;
- RPOS mechanism summary;
- required RPOS audit evidence groups and counts;
- `evidence_present` or `gap`;
- missing evidence groups;
- row-specific Not-Proven scope.

## Initial partial mappings

### Information / evaluation evidence

RPOS can retain bounded safety or capability evaluation evidence with source reference, source revision, declared scope, result summary, and optional artifact digest.

Presence of such evidence does not prove official certification, general AI safety, or legal/regulatory compliance.

### Human authority / accountability boundary

RPOS exposes Human Gate, declared authority, residual owner, and Human Return evidence separately from evaluation or execution evidence.

Presence of these records does not prove organizational governance sufficiency or legal responsibility allocation.

### Monitoring / external effect / recovery

RPOS separates execution receipts, external-effect readback, unresolved state, repair, resume, and residual responsibility.

The mapping reports a gap whenever any evidence group required by the bounded row is absent. A gap is an engineering evidence gap, not a legal non-compliance determination.

## Evidence-status semantics

`evidence_present` means only that the required RPOS evidence groups contain one or more records for the operation.

It does not mean:

- the evidence is sufficient for a regulator, auditor, customer, or organization;
- the evidence is correct or authentic beyond its declared provenance;
- the underlying guideline expectation is fully satisfied;
- the system is compliant, safe, or production-ready.

`gap` means one or more required RPOS evidence groups are currently empty. It is deliberately narrower than a compliance failure.

## Read-only rule

Generating the guideline matrix MUST NOT mutate operation state or event history. It MUST NOT approve, dispatch, reconcile, repair, resume, or otherwise create authority.

## Expansion rule

Future mapping rows should be added only when:

1. the relevant official expectation has been freshly verified;
2. the RPOS mechanism is identifiable;
3. the corresponding evidence class is executable or explicitly marked missing;
4. a Not-Proven boundary can be stated;
5. the row does not imply official endorsement or legal compliance.

The official checklist and worksheet may be used as structured source material in later iterations, but RPOS internal mapping identifiers remain independent engineering identifiers.

## International sequencing

NIST, ISO, EU, and other international profiles remain deferred until the Japanese operational profile and evidence vocabulary are stable. Later international mappings should reuse the same evidence classes rather than replace the Japan-first model.

## Not Proven

This mapping does not establish legal or regulatory compliance, official certification, audit sufficiency, production readiness, general AI safety, or correctness of external systems or evaluators.
