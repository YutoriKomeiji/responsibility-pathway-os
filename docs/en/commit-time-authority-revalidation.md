<!--
Document Title: RPOS Commit-Time Authority Revalidation
Document Type: Security Design Note
Status: Public-alpha candidate
Header Language: English
Body Language: English
-->

# RPOS Commit-Time Authority Revalidation

## Purpose

RPOS distinguishes **authority that existed earlier in a trajectory** from **authority that is still valid for the exact durable effect being committed now**.

`CommitAuthorityEnvelope` is an additive, opt-in security primitive for that durability boundary. It does not replace the existing RPOS state machine or `AuthorityEnvelope`.

## Bound values

A commit authority envelope binds:

- actor;
- operation id;
- action name;
- exact target digest;
- exact effect digest;
- evidence digest;
- context digest;
- issue and expiry times;
- authority epoch;
- one-shot consumption state.

`validate_commit_authority()` returns `HOLD` if any current value differs, if the authority has expired or is not yet valid, if the authority epoch is stale, or if the one-shot authority was already consumed.

## Why the authority epoch matters

An approval or capability can remain byte-for-byte unchanged while the governing authority state changes because of revocation, replacement, re-approval, or another policy transition. The `authority_epoch` is therefore compared against the caller-supplied current epoch at commit time.

RPOS does not define how an application increments or persists that epoch. The caller owns that policy and must provide the current value from an independently governed authority surface.

## One-shot authority

`consumed=True` fails closed. The primitive does not mutate the envelope or mark it consumed automatically; mutation/persistence semantics remain the responsibility of the integrating application.

This separation is deliberate so a validation helper cannot silently become an authority store.

## Security boundary

A successful validation means only that the supplied commit authority envelope matches the exact current values checked by the caller. It does **not** prove:

- that the evidence is true or sufficient;
- that the target system will perform the requested effect correctly;
- that the Human Gate was substantively justified;
- that the caller supplied an authentic authority epoch;
- production readiness or legal/compliance status.

The primitive is intended to make stale/replayed/detached authority easier to reject at the last responsible moment before a durable effect.
