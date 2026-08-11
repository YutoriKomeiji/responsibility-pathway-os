<!-- RPOS-DOC-ID: RPOS-IP-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: incubator -->
<!-- RPOS-DOC-COUNTERPART: ../ja/defensive-provenance-and-design-around-readiness.md -->

# RPOS Defensive Provenance and Design-around Readiness v0.1

## Purpose

Preserve dated engineering evidence so a later qualified reviewer can reconstruct how an RPOS feature originated, what sources informed it, what public disclosures existed, and which implementation boundaries may be replaceable.

This layer is an engineering provenance mechanism. It is not a patent opinion, freedom-to-operate conclusion, invalidity analysis, prior-art sufficiency conclusion, or legal advice.

## 1. Core rule

Unpublished third-party patent claims are not RPOS design inputs.

RPOS engineering continues from its own Responsibility Pathway lineage, internal requirements, public standards or guidance, and general engineering sources. External third-party material may be recorded as context, comparison, or an explicitly declared dependency, but comparison material does not silently become a normative feature rationale.

## 2. Provenance record

A provenance record identifies at least:

- record ID
- feature ID and name
- first-known internal date
- technical rationale
- source class
- source references
- external-reference boundary
- design-around readiness

Optional fields can record a first-known internal reference, public-disclosure date/reference, replaceable implementation boundary, and bounded notes.

## 3. Source classes

The initial source classes are:

- `internal_engineering`
- `public_standard_or_guidance`
- `general_engineering`
- `external_comparison`
- `declared_dependency`

The classification records provenance context; it does not determine novelty, inventive step, patent validity, or infringement.

## 4. External-reference boundary

External references are classified as:

- `none`
- `context_only`
- `comparison_only`
- `declared_dependency`

The purpose is to distinguish an engineering dependency from material that was merely observed or compared.

## 5. Design-around readiness

The initial states are:

- `not_assessed`
- `modular_boundary`
- `coupled_review_required`

`modular_boundary` requires the replaceable boundary to be named. This is architectural metadata only. It does not mean that replacing the component would avoid a patent claim.

## 6. Public disclosure metadata

When a public-disclosure date is recorded, the corresponding public reference is required, and vice versa. A date/reference pair is evidence of a recorded disclosure event, not a conclusion that the disclosure is legally effective prior art.

## 7. Future claim-chart use

Claim-chart analysis is not generated from unpublished or guessed claims. After an actual published or issued claim becomes available, a qualified reviewer may use the provenance record, repository history, public disclosures, and implementation boundaries as inputs to a separate claim-by-claim analysis.

That later analysis remains outside the normative responsibility-state machine.

## 8. Operational isolation

Defensive provenance data does not authorize, dispatch, verify, resume, deny, repair, or complete an RPOS operation. It does not create authority and does not modify responsibility state.

## 9. Fail-closed serialized import

Serialized provenance input rejects unknown fields. Fields that directly encode legal conclusions such as non-infringement, invalidity, freedom to operate, or prior-art sufficiency are prohibited from this engineering schema.

## 10. Documentation propagation

Changes to provenance semantics require review of:

- this JA/EN specification pair
- provenance schema/model/tests
- release-readiness documentation
- package/IP review procedure
- future Expert Review Pack interfaces where relevant
- public claim-chart workflow after it exists

Any deferred propagation must preserve an issue, Residual Owner, reason, affected artifact, and Human Return Point.

## Not Proven

This specification does not prove:

- patent non-infringement
- patent invalidity
- freedom to operate
- prior-art sufficiency
- novelty or inventive step
- legal meaning of a publication date
- completeness of engineering provenance
- that a named modular boundary will provide an effective design-around
