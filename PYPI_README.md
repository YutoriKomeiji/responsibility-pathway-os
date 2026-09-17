# RPOS — Responsibility Pathway Operating System

Version: **0.1.0a4**

RPOS is an open-source Python/SQLite runtime for AI agents and automation that perform consequential external actions. It keeps authorization, dispatch, external-effect uncertainty, verification, repair, resumption, Human Return, and Responsibility Routing connected as explicit responsibility state.

## Install

```bash
python -m pip install responsibility-pathway-os==0.1.0a4
rpos --db rpos.db boot
```

## What RPOS separates

- Human approval from execution authority.
- Dispatch from verified external effect.
- Transport/API receipt from evidence of real-world completion.
- Repair readiness from resume authority.
- Responsibility Routing from Authority grant.
- Unresolved external effects from false completion or blind retry.

## Responsibility Routing

RPOS classifies bounded next routes such as Human Gate, reconciliation hold, repair, and return-for-authorization. Route selection does not create legal, organizational, or execution Authority.

## Verification and scope

The project includes executable Python/SQLite tests, Windows and Ubuntu compatibility checks, deterministic integration scenarios, reproducible release evidence, SBOM generation, and selected Lean 4 machine-checked responsibility invariants.

These bounded checks do **not** establish production readiness, legal/compliance certification, universal safety, arbitrary third-party correctness, or implementation-wide formal correctness.

## Project links

- Source: https://github.com/YutoriKomeiji/responsibility-pathway-os
- PyPI: https://pypi.org/project/responsibility-pathway-os/
- Product site: https://yutorikomeiji.github.io/responsibility-pathway-os/

MIT License.
