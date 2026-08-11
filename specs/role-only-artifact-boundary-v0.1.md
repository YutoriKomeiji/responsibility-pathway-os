# RPOS Role-Only Artifact Boundary v0.1

Status: Private RPP Development Rule

## Purpose

Keep RPOS technical artifacts independent from private conversational identity systems and relationship-specific naming.

## Rule

RPOS specifications, reviews, README material, examples, tests, issue-facing technical text, and release-oriented artifacts use functional role, authority, component, and review-dimension labels only.

Private conversational identities and relationship-specific labels are outside the RPOS artifact boundary and must not be used as technical actors, reviewers, authorities, owners, return points, filenames, or attribution labels.

## Review artifacts

Review files use generic filenames ending in `-internal-review.md`.

Structured review sections use review dimensions rather than named reviewers. Accepted dimensions include:

- Integration Review
- Terminology Review
- Verification Review
- Human Usability Review
- Restart / Continuity Review
- Alternative Framing Review
- Implementation Review
- Provenance Review
- Boundary Review

The review conclusion belongs to the artifact and evidence record, not to a private identity label.

## Example and test actors

Executable examples and fixtures use generic role tokens such as:

- `requester`
- `executor`
- `human_authority`
- `operator`
- `residual_owner`

Human Return Point values use functional descriptions rather than identity names.

## Prevention

Focused tests enforce the RPOS review filename convention, the structured review heading vocabulary, and the generic actor vocabulary used by the executable Quick Start.

This rule does not require a repository copy of private identity names. The boundary is enforced positively through allowed RPOS vocabulary and artifact structure.
