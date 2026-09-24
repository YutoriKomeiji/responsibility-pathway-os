# Agent instructions for Responsibility Pathway Operating System

This file is the agent-facing routing surface for RPOS repository work. It does not replace current product documentation, release state, or formal-assurance sources.

## Read first

Before editing RPOS, fresh-read:

1. `README.md`
2. `product-status.json`
3. `CONTRIBUTING.md`
4. the exact source/spec/document/site surface affected by the task
5. `docs/en/claim-boundary-promotion.md` when public claim strength or maturity is involved
6. `docs/en/public-alpha-evaluation-guide.md` or the Japanese counterpart for evaluator-facing work
7. `docs/en/formal-assurance-surface.md` and `formal/assurance-catalog.json` when formal claims are involved

Do not substitute memory for current repository state.

## Repository role

RPOS is a public Python/SQLite responsibility-state runtime with product-site, demo, integration, and bounded formal-assurance surfaces.

## Surface projection

- README / product site: product purpose, current behavior, install/use path, material limits, concise factual machine-readable context.
- Evaluation guide: how an evaluator should inspect evidence and report results.
- Formal assurance viewer/catalog: theorem/runtime-test/model-scope/proof-ceiling relationships.
- Demo surfaces: what is actually executed, simulated, observed, and not demonstrated.
- Structured manifests: stable machine-readable release/claim/evidence state.
- Source comments: local semantic invariants and misuse-prevention boundaries.

A Proof Ceiling is appropriate on a formal-assurance surface. It should not be repeated mechanically on unrelated product prose.

## Currentness and parity

Treat currentness as part of correctness.

Check:
- current published version vs README/site/evaluation guide;
- EN/JA counterpart parity;
- product-status vs prose claims;
- source demo vs published-package identity;
- formal catalog vs viewer/source references.

Historical records should remain historical rather than being rewritten to mimic the current release.

## Evidence and claims

Keep evidence proportional to its source. A Lean theorem proves only the declared model property; linked Python tests are separate implementation evidence; neither automatically establishes deployment, legal, organizational, or external-world truth.

Prefer positive scope/ownership descriptions when equivalent. Keep explicit negative statements where they prevent a concrete over-reading.

## Human-gated actions

Do not autonomously publish packages/releases, change repository visibility/permissions/credentials, promote production/legal/compliance claims, or change Authority/canonical semantics without explicit approval.

## GitHub Actions preflight

Before making a change that may trigger GitHub Actions:

1. Identify the workflows triggered by the target paths and event.
2. Inspect the relevant workflow definitions before changing files. If the workflow has not run recently, especially after several days, also inspect its latest runs and recent failure history before triggering it again.
3. Check referenced action/runtime versions, dependency-install behavior, runner assumptions, and obvious deprecation or staleness risks.
4. Check freeze, release, candidate, publication, branch, path-filter, and other repository-specific gates before changing a governed path.
5. Keep mutually dependent source, test, schema, generated, or fixture changes atomic where practical so an intermediate commit does not create avoidable red runs.
6. After the change, read back every workflow triggered by that change to a terminal state. Do not report the change as green while relevant runs are queued or in progress.
7. Treat historical failed runs as retained evidence. Do not rerun, erase, or cosmetically replace them only to make the Actions UI green.

A passing workflow proves only the scope asserted by that workflow. It does not replace repository-specific Authority, release, publication, or evidence gates.
