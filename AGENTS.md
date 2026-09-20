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
