<!-- RPOS-DOC-ID: RPOS-IP-002 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: incubator -->
<!-- RPOS-DOC-COUNTERPART: ../ja/public-claim-review-readiness.md -->

# RPOS Public Claim Review Readiness v0.1

## Purpose

Prepare RPOS for later claim-by-claim review after a third-party patent application or patent becomes publicly available, without guessing unpublished claims or treating third-party patent strategy as an RPOS design input.

## Recorded metadata

A public-claim review record may preserve:

- publication number and publication date;
- application number where known;
- priority date where known;
- exact claim identifier and public claim-text reference;
- issued patent number and issued-claim version where applicable;
- RPOS feature identifiers selected for qualified comparison;
- engineering review status and notes.

A record cannot exist without a public publication identifier, publication date, claim identifier, and public claim-text reference.

## Review lifecycle

Engineering review uses bounded statuses:

- `not_started`
- `public_claim_available`
- `qualified_review_required`
- `design_around_review`
- `closed_no_engineering_change`
- `closed_engineering_change`

These are workflow statuses, not legal conclusions.

## Design-around principle

When a qualified review identifies a material engineering overlap risk, RPOS should first inspect declared replaceable boundaries. The preferred response is a bounded module or algorithm replacement that preserves Responsibility Pathway semantics rather than a broad rewrite of the operating system.

## Separation from legal conclusions

The report always leaves the following Not Proven:

- patent non-infringement;
- patent invalidity;
- freedom to operate;
- prior-art sufficiency;
- claim scope;
- legal advice.

RPOS preserves dated engineering inputs. Qualified reviewers make legal conclusions outside this engineering schema.
