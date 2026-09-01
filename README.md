<!-- RPOS-DOC-ID: RPOS-PUBLIC-README-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1.0a2 -->
<!-- RPOS-DOC-STATUS: public-alpha-published -->
<!-- RPOS-DOC-COUNTERPART: README.ja.md -->

# RPOS — Responsibility Pathway Operating System

[![Standalone Verification](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/standalone-verify.yml/badge.svg?branch=main)](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/standalone-verify.yml)
[![Formal Assurance](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/formal-assurance.yml/badge.svg?branch=main)](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/formal-assurance.yml)
[![Field Portability](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/field-portability.yml/badge.svg?branch=main)](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/field-portability.yml)
[![PyPI](https://img.shields.io/pypi/v/responsibility-pathway-os?label=PyPI)](https://pypi.org/project/responsibility-pathway-os/)
[![Python](https://img.shields.io/pypi/pyversions/responsibility-pathway-os)](https://pypi.org/project/responsibility-pathway-os/)
[![License](https://img.shields.io/github/license/YutoriKomeiji/responsibility-pathway-os)](LICENSE)

**Keep uncertain external effects explicit until verification, repair, or a new authorization resolves them.**

RPOS is an open-source Python/SQLite runtime for AI agents and automation that perform consequential external actions. It keeps authorization, dispatch, external effect, verification, repair, resumption, and Human Return connected as executable responsibility state.

## Why use RPOS?

An agent can receive a timeout after an external system has already changed. A blind retry may duplicate a payment, deployment, message, permission change, or other real-world effect.

RPOS keeps those states separate instead of collapsing them into a single “success” or “failure.”

- **Human approval is not permanent execution authority.**
- **Dispatch is not verified external effect.**
- **A successful receipt is not proof of reality.**
- **Unknown stays unknown.** `EFFECT_UNKNOWN` preserves unresolved post-dispatch state.
- **Recovery keeps an owner.** Repair, reconciliation, resumption, and Human Return remain connected to the same responsibility pathway.

## Quick Start

Version: **0.1.0a2** — current published release.

```bash
python -m pip install responsibility-pathway-os==0.1.0a2
rpos --db rpos.db boot
```

- [PyPI 0.1.0a2](https://pypi.org/project/responsibility-pathway-os/0.1.0a2/)
- [Product site](https://yutorikomeiji.github.io/responsibility-pathway-os/)
- [Japanese launch article](https://zenn.dev/dantarg/articles/rpos-public-alpha-010a2)

`0.1.0a2` is an evolving 0.x release, but its documented public surfaces can be tried within their stated boundaries. The three production-grade integration demos on current `main` were added after the published release, so run those from a source checkout.

## What is implemented now

- durable responsibility state in Python/SQLite;
- explicit Human Gate and operational-authority boundaries;
- bounded dispatch attempts, restart, reconciliation, repair, resume, and Human Return;
- external-effect separation so a successful transport receipt does not silently become completion;
- CLI and executable scenarios;
- Responsibility State Envelope templates with `authority_effect: "none"`;
- reproducible public export, SBOM, and release evidence;
- Windows/Python field-portability checks;
- selected responsibility invariants machine-checked in Lean 4.

## Operational state model

Core states:

`PROPOSED`, `HUMAN_GATE`, `AUTHORIZED`, `DISPATCHING`, `EFFECT_UNKNOWN`, `VERIFIED`, `REPAIR_REQUIRED`, `READY_TO_RESUME`, `COMPLETED`, `DENIED`, `ABORTED`.

Key distinctions:

- `AUTHORIZED` means the conditions for action are present; it does not mean execution has started or succeeded.
- `DISPATCHING` preserves an issued but unresolved attempt.
- `EFFECT_UNKNOWN` preserves uncertainty instead of reporting false success.
- `REPAIR_REQUIRED` means the pathway must be repaired or reviewed before continuing.
- `READY_TO_RESUME` means repair readiness, not permission to execute.
- `COMPLETED` follows bounded verification, not merely a transport receipt.

A model proposal is not operational authority. Human approval also does not become unlimited retry or resume authority after failure.

## Executable examples

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

These examples cover bounded paths for Human Gate decisions, `EFFECT_UNKNOWN`, restart, reconciliation, repair, explicit resume authority, replay protection, adapter exceptions, and Human Return.

## Integration demo suite

Current `main` also includes `examples/production_grade_demos/`:

```bash
python examples/production_grade_demos/run_demo.py
```

Scenarios include:

- **supplier payment ambiguity** — an external service commits the payment and drops the connection; RPOS enters `EFFECT_UNKNOWN`, survives process restart, verifies the effect through independent readback, and avoids duplicate dispatch;
- **production deployment rejection and repair** — external rejection enters `REPAIR_REQUIRED`, a fresh human resume authorization is required, and completion follows readback rather than receipt alone;
- **privileged-access revocation denial** — Human Gate denial leaves the external side-effect count at zero.

The localhost service is a deterministic integration fixture, not a real payment processor, production controller, or IAM provider. Passing these demos proves only the declared paths in the tested environment.

## Lean 4 assurance surface

RPOS publishes a theorem-to-runtime-test crosswalk in `formal/assurance-catalog.json`.

Current machine-checked assertions include:

1. a Human Gate cannot dispatch directly;
2. only `VERIFIED` may directly enter `COMPLETED`;
3. unresolved `EFFECT_UNKNOWN` is not completion;
4. repair readiness is not execution authority;
5. a transport/API receipt is not external-effect verification;
6. a model proposal is not operational authority.

These are Lean 4 theorems over declared bounded models. They do not prove the entire Python runtime, deployment environment, legal responsibility, organizational authority, or arbitrary external systems.

## Support status and known limits

RPOS can be used today for engineering evaluation and bounded integrations within its documented surfaces. The current release is not designed to be a self-contained control plane for unattended high-impact production operation.

RPOS does not by itself provide or guarantee:

- legal or organizational authority;
- correctness of arbitrary external systems;
- universal exactly-once behavior;
- external-effect proof from a receipt alone;
- compatibility with every production environment;
- implementation-wide formal proof of the Python runtime.

When an environment, attack case, failure mode, or integration gap is discovered, the project treats it as input to the OSS improvement loop rather than as a reason to hide the software from use.

- [Security](SECURITY.md)
- [Support](SUPPORT.md)
- [Contributing](CONTRIBUTING.md)

## Claim boundaries

RPOS separates evidence-limited claims that may improve from permanent responsibility boundaries that software should not cross by itself. See `docs/en/claim-boundary-promotion.md`.

Version age alone does not promote a claim. Stronger claims require implementation, scoped evidence, and review.

## Project surfaces

- PyPI: `responsibility-pathway-os==0.1.0a2`
- GitHub Pages product site and architecture maps
- `site/assurance.html` — Formal Assurance Viewer
- `formal/assurance-catalog.json` — theorem/runtime-test crosswalk
- `product-status.json` — machine-readable release and claim state
- `examples/production_grade_demos/` — current-main integration suite
- `CHANGELOG.md` — release history

## License

MIT License.
