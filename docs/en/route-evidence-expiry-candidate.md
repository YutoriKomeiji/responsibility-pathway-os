# Expiring route evidence — bounded source candidate

The opt-in `assess_route_receiver` helper accepts `assessed_at` and `evidence_expires_at` together as timezone-aware Python `datetime` values. At or after expiry, eligibility is `ineligible` and the effective route is `neutral_hold`, even if the caller supplies positive host-side checks. Missing one timestamp or naive timestamps raise `ValueError`.

Expiry is a caller-supplied validity bound, **not verified authority**. The caller must establish the underlying evidence's provenance and trust independently; a clock or expiration timestamp does not authenticate the receiver. This helper does not auto-route or issue/revoke execution permissions. Reassess with current host truth on each consequential handoff and after process restart. The existing assessment-history event is a historical observation, never a cached authorization token.

This is unreleased source work until a separately gated version transition, and no full implementation-wide formal proof is claimed.
