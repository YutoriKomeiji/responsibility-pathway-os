<!--
Document Title: RPOS Public Alpha Evaluation Guide
Document Type: Public Product Evaluation Guide
Status: Public Alpha Candidate
Header Language: English
Body Language: English
-->

# RPOS Public Alpha Evaluation Guide

## Purpose

RPOS 0.1.0a1 is intended for engineering evaluation and bounded pilots. This guide gives an evaluator a short route from clean installation to the responsibility boundaries that distinguish RPOS from an ordinary retry wrapper or workflow logger.

The goal is not to demonstrate universal safety or production readiness. The goal is to make the implemented behavior easy to inspect, reproduce, criticize, and compare against the documented claims.

## Fifteen-minute evaluation route

From a clean Python 3.11+ environment:

```bash
python -m pip install responsibility-pathway-os==0.1.0a1
rpos --db rpos.db boot
```

For a source candidate before PyPI publication:

```bash
python -m pip install .
python examples/quick_start_end_to_end.py
```

Then run the focused examples:

```bash
python examples/happy_path_verified.py
python examples/human_gate_denied.py
python examples/effect_unknown_restart_reconcile.py
python examples/quick_start_end_to_end.py
python examples/idempotency_replay_guard.py
python examples/human_return_reauthorization.py
python examples/adapter_exception_containment.py
python examples/reconciliation_unresolved_human_return.py
```

## What each example is evidence for

- `happy_path_verified.py`: a bounded verified path can reach completion after the declared verification contract is satisfied.
- `human_gate_denied.py`: denied Human Gate decisions do not dispatch.
- `effect_unknown_restart_reconcile.py`: a successful transport receipt is not promoted into external-effect proof; restart preserves uncertainty until reconciliation.
- `quick_start_end_to_end.py`: repair readiness remains separate from resume authority and a fresh attempt remains separately observable.
- `idempotency_replay_guard.py`: repeating the same idempotency/effect key does not silently redispatch the recorded semantic effect.
- `human_return_reauthorization.py`: responsibility moves to the declared repair owner and then back to the declared resume authority instead of being restored implicitly.
- `adapter_exception_containment.py`: an adapter exception after dispatch begins is contained as external-effect uncertainty rather than treated as proof that nothing happened.
- `reconciliation_unresolved_human_return.py`: an unavailable independent observer preserves `EFFECT_UNKNOWN` and an explicit Human Return Point.

These examples are bounded executable evidence. They are not evidence that every adapter, external system, organizational policy, or deployment will behave correctly.

## Formal evidence route

The bounded Lean 4 model is independently reproducible from the formal directory:

```bash
cd formal/lean
lake build
```

The repository pins Lean 4.32.2 for this surface. The current formal project checks the declared state, reachability, evidence, Responsibility State Envelope, operational, and transparency boundaries.

A successful `lake build` proves only the encoded model under its stated assumptions. It does not prove the Python implementation, real-world external effects, authority validity, legal validity, organizational responsibility, or production safety.

## Field-quality route

The release-candidate verification checks source tests, all examples, wheel and sdist clean installation, installed CLI/API boundaries, CycloneDX SBOM generation, source-bound public-export evidence, and likely-secret scanning. A separate field-portability workflow exercises CLI/recovery boundaries on Windows with Python 3.11 and 3.12.

If a failure occurs after a possible external dispatch, preserve the operation state and evidence before attempting a retry. The absence of a response is not evidence that the external effect did not occur.

## RPOS and RPR

RPR (Responsibility Pathway Runtime) is the narrower runtime layer for preserving an execution attempt, external-effect ambiguity, readback evidence, restart continuity, and Human Return around consequential writes.

RPOS is the broader responsibility operating layer. It includes authority/Human Gate state, evidence classes, responsibility-state envelopes, recovery/resume responsibility, observability, provenance, and formal/public-claim boundaries around the executable core.

For a narrowly scoped write/reconcile runtime integration, RPR may be the smaller starting point. For evaluation of the broader responsibility-state operating model, use RPOS. Neither package creates organizational authority merely by being installed.

## Useful project surfaces

- `README.md` / `README.ja.md`: first product overview and install route.
- `product-status.json`: machine-readable release stage, verified surfaces, non-claims, and release gates.
- `CHANGELOG.md`: release-candidate changes and deferred areas.
- `SECURITY.md`: security reporting and supported boundary.
- `CONTRIBUTING.md`: contribution and evidence discipline.
- `SUPPORT.md`: alpha support expectations.
- `docs/en/public-claim-evidence-crosswalk.md`: public claims mapped to implementation/evidence boundaries.
- `docs/en/os-quality-readiness.md`: product-quality scope and explicit alpha deferrals.

## Evaluation return path

Useful feedback includes reproducible failures, counterexamples, confusing state transitions, unsafe retry incentives, missing integration boundaries, portability failures, documentation mismatches, and claims that appear stronger than the available evidence.

Negative results are useful evidence. RPOS should become stronger through reproduction, criticism, field use, and repair rather than through self-certification.
