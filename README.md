<!-- RPOS-DOC-ID: RPOS-PUBLIC-README-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1.0a2 -->
<!-- RPOS-DOC-STATUS: public-alpha-published -->
<!-- RPOS-DOC-COUNTERPART: README.ja.md -->

# RPOS — Responsibility Pathway Operating System

**Executable responsibility pathways in Python, with critical responsibility invariants machine-checked in Lean 4.**

RPOS is an independently engineered, open-source Responsibility Pathway OS for consequential AI and automation workflows. It combines a Python/SQLite executable runtime with a Lean 4 Formal Assurance Surface for selected invariants covering Human Gate, operational authority, dispatch, external-effect verification, uncertainty, recovery, resumption, and completion.

> **Project identity / attribution:** RPOS is independently developed within the Responsibility Pathway lineage by the `YutoriKomeiji/responsibility-pathway-os` project. It is **not** developed by, affiliated with, or an implementation of GhostDrift Mathematical Institute or its "Responsibility OS" work. Similar terminology does not imply common authorship, ownership, or lineage.

RPOS is not a model wrapper, a policy document, or a logging layer. It keeps responsibility-bearing state executable across:

`proposal -> Human Gate -> authorization -> dispatch -> effect verification -> uncertainty -> repair -> explicit resumption -> completion`

Its core rule is simple: **authorization is not execution, an execution receipt is not proof of external effect, and failure or uncertainty must not erase responsibility.**

## What is implemented now

The public alpha includes:

- a Python/SQLite operational state machine with durable responsibility state;
- explicit Human Gate and operational-authority boundaries;
- bounded dispatch attempts, restart/reconciliation, repair/resume, and Human Return;
- external-effect separation so a successful transport receipt does not silently become completion;
- CLI and executable evaluation scenarios;
- Responsibility State Envelope templates with `authority_effect: "none"`;
- reproducible public-export, SBOM, and release-evidence generation;
- Windows/Python field-portability checks; and
- a reproducible Lean 4 project machine-checking selected responsibility invariants.

## Python × Lean 4 — executable responsibility with machine-checked invariants

RPOS exposes a public theorem-to-runtime-test crosswalk in `formal/assurance-catalog.json`:

`operational risk -> Lean theorem -> Python runtime test -> model scope -> proof ceiling`

Current machine-checked assertions include:

1. `RPOS.human_gate_cannot_dispatch_directly` — a Human Gate is not direct dispatch authority;
2. `RPOS.only_verified_enters_completed` — only `VERIFIED` may directly enter `COMPLETED`;
3. `RPOS.effect_unknown_is_not_completed` — unresolved external-effect uncertainty is not completion;
4. `RPOS.ready_to_resume_is_not_authorized` — repair readiness is not execution authority;
5. `RPOS.receipt_is_not_effect_verification` — a transport/API receipt is not external-effect verification;
6. `RPOS.model_proposal_is_not_authority` — a model proposal is not operational authority.

These are real Lean 4 theorems over declared bounded models. They do **not** imply that the entire Python runtime, deployment environment, legal responsibility, organizational authority, or arbitrary external system is formally proven.

That boundary is deliberate: formal proof, executable implementation evidence, and real external-effect evidence are different evidence classes and must not impersonate one another.

## Independent Responsibility Pathway lineage

RPOS is independently engineered within the Responsibility Pathway lineage:

```text
Responsibility Pathway Model / Paper
  -> Responsibility Pathway Design
  -> Responsibility Pathway Engineering
  -> Responsibility Pathway Runtime
  -> RPOS — Responsibility Pathway Operating System
  -> formal + executable + operational evidence
  -> upstream revision
```

The lineage centers on responsibility continuity across judgment, authorization, execution, uncertainty, repair, return, resumption, and residual ownership. RPOS is the operating layer: **RPOS owns operation, not intelligence.** Models remain replaceable proposal sources; they do not become authority merely by proposing an action.

## Public Alpha status

Version: **0.1.0a2 — Early Public Alpha / Executable Preview**

`responsibility-pathway-os==0.1.0a2` was published to PyPI on **2026-08-29** through PyPI Trusted Publishing and is the current public alpha release. Python 3.11+ is required.

```bash
python -m pip install responsibility-pathway-os==0.1.0a2
rpos --db rpos.db boot
```

For evaluation from the current repository source:

```bash
python -m pip install -e .
python examples/quick_start_end_to_end.py
```

This alpha is intended for engineering evaluation and bounded pilots, not unattended production operation.

## Why RPOS exists

Agent systems can receive a successful tool/API receipt while the real-world effect is absent, partial, duplicated, ambiguous, or unverifiable. They can also lose the human decision boundary during retry or recovery.

RPOS keeps those cases explicit:

- `AUTHORIZED` does not mean execution has started or succeeded.
- `DISPATCHING` preserves an issued but unresolved attempt.
- `EFFECT_UNKNOWN` preserves uncertainty instead of reporting false success.
- `REPAIR_REQUIRED` makes recovery responsibility explicit.
- `READY_TO_RESUME` means repair readiness, not permission to execute.
- explicit resumption restores authority before a fresh dispatch attempt.
- `COMPLETED` follows bounded verification, not merely a transport receipt.

## Core responsibility states

`PROPOSED`, `HUMAN_GATE`, `AUTHORIZED`, `DISPATCHING`, `EFFECT_UNKNOWN`, `VERIFIED`, `REPAIR_REQUIRED`, `READY_TO_RESUME`, `COMPLETED`, `DENIED`, `ABORTED`.

## Executable examples

The repository includes eight compact executable scenarios:

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

They exercise bounded paths for approval/denial, `EFFECT_UNKNOWN`, restart, reconciliation, repair, explicit resume authority, replay protection, adapter exceptions, and Human Return. They are executable evidence for those scenarios only.

## Production-grade operational demo suite

Current `main` also includes executable integration scenarios under `examples/production_grade_demos/`. These were added **after** the PyPI `0.1.0a2` artifacts were published, so the demo source itself is not claimed to be contained in the published `0.1.0a2` wheel/sdist. Run it from a current source checkout:

```bash
python examples/production_grade_demos/run_demo.py
```

The suite uses the shipped `RposService` and RPOS SQLite persistence/transition logic while a separate localhost HTTP process writes effects to a separate SQLite database. It does not copy or reimplement the RPOS state machine.

The three scenarios cover:

- **supplier payment ambiguity** — the external service commits a payment and drops the connection; RPOS enters `EFFECT_UNKNOWN`, a real Python process restart occurs, independent readback confirms the effect, and no duplicate dispatch is required;
- **production deployment rejection and repair** — external rejection enters `REPAIR_REQUIRED`, explicit human resume authority is required, a fresh dispatch identity is used, and completion follows independent readback rather than receipt alone;
- **privileged-access revocation denial** — Human Gate denial leaves the external side-effect count at zero.

The localhost service is a deterministic integration fixture, not a real payment processor, production controller, or IAM provider. Passing these demos verifies the declared paths in the tested environment; it does not establish production readiness or arbitrary external-system correctness.

## Lean 4 Formal Assurance Surface

The formal project is pinned to **Lean 4.32.2**.

```bash
cd formal/lean
lake build
```

Current modules include:

- `RPOSState.lean` — state transitions, Human Gate, completion, uncertainty, resume authority;
- `RPOSReachability.lean` — bounded multi-step reachability and no-direct-shortcut properties;
- `RPOSEvidenceBoundary.lean` — separation among authorization, receipt, verification, evaluation, and dependency evidence;
- `RPOSPacketBoundary.lean` — no-authority-effect properties for responsibility envelopes;
- `RPOSOperationalBoundary.lean` — model proposal, human authorization, receipt, external observation, and operational responsibility;
- `RPOSTransparencyBoundary.lean` — transparency/evidence distinctions.

The public Formal Assurance Viewer is generated from the exact site commit after the Lean project is machine-checked and maps operational risks to theorem names, Python runtime tests, source identity, model scope, and proof ceiling.

## Responsibility State Envelope

`templates/catalog.json` contains reusable neutral-role templates for operation proposal, Human Gate decision, verification contract, repair plan, resume authorization, dependency evidence, external evaluation evidence, and Human Return.

Every envelope has `authority_effect: "none"`: **creating or validating an envelope never authorizes, dispatches, verifies, completes, or resumes an operation.**

## Verification route

The release route includes:

- the complete Python test suite;
- all eight compact source examples;
- wheel and sdist build and clean-install checks;
- installed CLI/API checks outside the repository working directory;
- exact-HEAD public-export reconstruction;
- source-bound CycloneDX SBOM and SHA-256 release evidence;
- public-source likely-secret scanning;
- Windows and Ubuntu checks on Python 3.11 and 3.12;
- pinned Lean 4 `lake build`;
- exact-head Formal Assurance manifest generation; and
- GitHub Pages validation and deployment with machine-checked assurance and verified architecture visuals.

The current-main production-grade demo suite is additionally exercised by the repository test/CI route after its introduction.

Passing those checks establishes the named engineering evidence within their declared scope. It does not automatically establish production readiness, legal compliance, universal safety, organizational authority, arbitrary external-system correctness, or implementation-wide formal correctness.

## Claim boundary and promotion

RPOS separates two different things:

- **Current Evidence Boundaries** — claims that may advance when declared evidence is obtained and reviewed;
- **Permanent Responsibility Boundaries** — authority or responsibility that software should not create by itself.

Evidence-limited claims currently include production readiness, broader platform support, implementation-wide formal conformance, stronger software-supply-chain trust, and domain effectiveness beyond the published scenarios.

Permanent boundaries include legal/regulatory authority, correctness of arbitrary external systems, receipt-as-effect proof without a verification contract, transfer of final organizational responsibility to software, and universal exactly-once guarantees for arbitrary systems lacking the required contract.

See `docs/en/claim-boundary-promotion.md`.

## Direction

The long-term goal is larger than the current alpha: make responsibility-bearing operational state easier to execute, inspect, test, formally reason about, recover, and return to accountable humans or institutions across real AI-enabled workflows.

That is a goal, not a claim of completion. Each stronger public claim must earn its promotion through implementation, evidence, and review.

## Project surfaces

- PyPI: `responsibility-pathway-os==0.1.0a2`
- GitHub Pages product site and architecture maps
- `site/assurance.html` — Formal Assurance Viewer
- `formal/assurance-catalog.json` — canonical theorem/runtime-test crosswalk
- `product-status.json` — machine-readable release and claim state
- `examples/production_grade_demos/` — current-main executable integration suite
- `docs/en/public-alpha-evaluation-guide.md` — third-party evaluation route
- `CHANGELOG.md` — release history
- `SECURITY.md`, `SUPPORT.md`, `CONTRIBUTING.md`

## License

MIT License.
