<!-- RPOS-DOC-ID: RPOS-PUBLIC-README-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1.0a1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: README.ja.md -->

# RPOS — Responsibility Pathway Operating System

RPOS is an executable responsibility operating layer for consequential AI and automation workflows.

Its core rule is: **authorization is not execution, an execution receipt is not proof of external effect, and failure or uncertainty must not erase responsibility.**

RPOS preserves a responsibility pathway across:

`proposal -> Human Gate -> authorization -> dispatch -> effect verification -> uncertainty -> repair -> explicit resumption -> completion`

## Public alpha status

Version: **0.1.0a1 candidate — Early Public Alpha / Executable Preview**

The current implementation provides a Python/SQLite executable core, durable responsibility state, Human Gate handling, bounded dispatch attempts, external-effect separation, reconciliation, repair/resume, evidence history, reusable Responsibility State Envelopes, guideline/evidence views, provenance support, a CLI, runnable examples, and a bounded machine-checked Lean formal model.

This alpha is intended for engineering evaluation and bounded pilots, not unattended production use.

## Why RPOS exists

Agent systems can produce a successful tool receipt while the real-world effect is absent, partial, duplicated, ambiguous, or unverifiable. They can also lose the human decision boundary when retrying after failure.

RPOS keeps those cases explicit:

- `AUTHORIZED` does not mean execution has started or succeeded.
- `DISPATCHING` preserves an issued but unresolved attempt.
- `EFFECT_UNKNOWN` preserves uncertainty instead of reporting false success.
- `REPAIR_REQUIRED` makes recovery responsibility explicit.
- `READY_TO_RESUME` means repair readiness, not permission to execute.
- resumption restores authority before a fresh dispatch attempt.
- `COMPLETED` follows bounded verification, not merely a transport receipt.

## Install

Python 3.11+ is required.

```bash
python -m pip install responsibility-pathway-os==0.1.0a1
rpos --db rpos.db boot
```

For a source checkout:

```bash
python -m pip install -e .
python examples/quick_start_end_to_end.py
```

For a short evaluator route covering executable, formal, and field-quality boundaries, see `docs/en/public-alpha-evaluation-guide.md`.

## Executable examples

The public alpha candidate includes eight executable evaluation scenarios:

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

They cover:

1. Human Gate approval followed by bounded independent verification and completion;
2. Human Gate denial with no dispatch;
3. successful receipt -> `EFFECT_UNKNOWN` -> process restart -> observation-only reconciliation -> completion;
4. failed first attempt -> `REPAIR_REQUIRED` -> repair preparation -> `READY_TO_RESUME` -> explicit resume authorization -> fresh attempt -> `EFFECT_UNKNOWN` -> restart -> reconciliation -> completion;
5. duplicate idempotency/effect identity -> no silent redispatch of the recorded semantic effect;
6. repair responsibility -> explicit Human Return -> explicit resume authority rather than implicit authority restoration;
7. adapter exception after dispatch begins -> `EFFECT_UNKNOWN` rather than proof that no external effect occurred;
8. unavailable reconciliation observer -> preserved `EFFECT_UNKNOWN` and explicit Human Return.

The examples are executable evidence for those bounded scenarios only.

## Responsibility State Envelope templates

`templates/catalog.json` contains reusable neutral-role templates for:

- operation proposal;
- Human Gate decision;
- verification contract;
- repair plan;
- resume authorization;
- dependency evidence;
- external evaluation evidence;
- Human Return packet.

The preferred `rpos.validate_envelope(...)` API rejects unknown fields, missing required fields, unsupported template kinds/schema versions, and any envelope that claims an authority effect.

Every Responsibility State Envelope has `authority_effect: "none"`: **filling or validating an envelope never authorizes, dispatches, verifies, completes, or resumes an operation.** The earlier `ResponsibilityPacket`, `validate_packet(...)`, and `rpos.packet.v0.1` names remain supported for backward compatibility. See `docs/en/responsibility-packet-templates.md`.

## Core responsibility states

`PROPOSED`, `HUMAN_GATE`, `AUTHORIZED`, `DISPATCHING`, `EFFECT_UNKNOWN`, `VERIFIED`, `REPAIR_REQUIRED`, `READY_TO_RESUME`, `COMPLETED`, `DENIED`, `ABORTED`.

The normative transition model intentionally prevents a success receipt from directly proving completion and prevents repair readiness from silently restoring execution authority.

## Bounded Lean 4 formal model

RPOS has a machine-checked formal evidence surface pinned to **Lean 4.32.2**. It is independently reproducible as a Lake project:

```bash
cd formal/lean
lake build
```

Current modules:

- `formal/lean/RPOSState.lean` — states, direct transitions, local invariants;
- `formal/lean/RPOSReachability.lean` — bounded multi-step reachability and no-direct-shortcut properties;
- `formal/lean/RPOSEvidenceBoundary.lean` — bounded separation among authorization-relevant evidence, external-effect-verification evidence, receipts, evaluations, and dependency evidence;
- `formal/lean/RPOSPacketBoundary.lean` — bounded no-authority-effect properties for responsibility envelopes/packets;
- `formal/lean/RPOSOperationalBoundary.lean` — bounded operational responsibility properties;
- `formal/lean/RPOSTransparencyBoundary.lean` — bounded transparency/evidence distinctions.

Examples of machine-checked properties include:

- only `AUTHORIZED` directly enters `DISPATCHING`;
- only `VERIFIED` directly enters `COMPLETED`;
- `EFFECT_UNKNOWN` cannot directly complete;
- `REPAIR_REQUIRED` cannot directly dispatch;
- `READY_TO_RESUME` restores authority through `AUTHORIZED`, not direct dispatch;
- execution receipts, evaluation evidence, and dependency evidence do not become external-effect verification evidence in the declared abstract model.

Positive reachability theorems are path-existence witnesses, not liveness guarantees.

**Formal proof evidence does not prove the Python implementation.** RPOS explicitly keeps formal proof, executable implementation evidence, and operational external-effect evidence separate. See `formal/lean/README.md`.

## Evidence boundaries

RPOS separates evidence classes instead of allowing one kind of evidence to impersonate another:

- authority and admission;
- execution / receipt;
- external effect;
- recovery and resume;
- safety / capability evaluation evidence;
- dependency / software-supply-chain evidence;
- guideline evidence matrices;
- engineering provenance and future public-claim review inputs.

Evidence recording does not automatically promote operational responsibility state unless the corresponding state-transition contract explicitly requires it.

## Defensive provenance

RPOS records engineering provenance so later qualified review can reconstruct when and why a feature was introduced and where implementation boundaries may be replaceable.

Unpublished third-party patent claims are not treated as design inputs. Public-claim review records require actual publication metadata and a public claim-text reference.

RPOS does **not** determine patent non-infringement, patent invalidity, freedom to operate, prior-art sufficiency, or legal claim scope.

## Japan-first development

The initial adoption profile is Japan-first. Current bounded evidence work references official Japanese AI and software-supply-chain guidance and preserves explicit gaps rather than emitting a compliance verdict.

International mappings are planned after the Japanese operating/profile layer stabilizes.

## Continuous development cycle

RPOS is developed as one layer of a continuous feedback system:

```text
Responsibility Pathway Model / Paper
  -> Responsibility Pathway Engineering
  -> Responsibility Pathway Runtime
  -> RPOS
  -> formal + executable + operational evidence
  -> Engineering + Model / Paper
```

A concept should move downstream into executable evidence and then return upstream as definitions, counterexamples, engineering obligations, limitations, or empirical questions. No layer may claim another layer's evidence.

## Verification

Current release-candidate verification includes:

- the full Python test suite;
- execution of all eight source examples;
- wheel and source-distribution builds;
- isolated clean installation of wheel and sdist;
- installed CLI/API and Quick Start checks outside the repository working directory;
- deterministic exact-HEAD public-export reconstruction;
- source-bound CycloneDX SBOM and SHA-256 release-artifact evidence;
- likely-secret scanning of the public source boundary;
- Windows field-portability checks on Python 3.11 and 3.12;
- pinned `lake build` verification of the declared bounded Lean 4 project.

Passing these checks is evidence within their declared scope. It does not establish production readiness, legal compliance, external-system correctness, universal safety, or implementation-wide formal correctness.

## Project surfaces

- `product-status.json` — machine-readable release stage, verified surfaces, non-claims, and release gates;
- `CHANGELOG.md` — public-alpha changes and explicit deferrals;
- `CONTRIBUTING.md` — contribution and evidence discipline;
- `SUPPORT.md` — alpha support expectations;
- `SECURITY.md` — security reporting and supported boundary;
- `docs/en/public-alpha-evaluation-guide.md` — short third-party evaluation route.

## Not Proven

RPOS 0.1.0a1 does not prove or claim:

- production or enterprise readiness;
- legal or regulatory compliance;
- certification or official conformity;
- universal AI safety;
- correctness of arbitrary remote adapters or credentials;
- exactly-once effects over arbitrary external systems;
- complete software-supply-chain trustworthiness;
- formal correctness/conformance of the Python implementation as a whole;
- liveness/eventual completion for arbitrary operations;
- patent non-infringement, patent invalidity, or freedom to operate.

## License

MIT License.

## Lineage

```text
Responsibility Pathway Design / Model
 -> Responsibility Pathway Engineering
 -> Responsibility Pathway Runtime
 -> RPOS — Responsibility Pathway Operating System
```

RPOS is independently engineered as the operating layer that preserves responsibility continuity through authority, execution, uncertainty, repair, and explicitly authorized resumption.
