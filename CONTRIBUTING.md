# Contributing to RPOS

RPOS welcomes reproducible bug reports, counterexamples, integration feedback, documentation corrections, and narrowly scoped code changes.

## Before opening a change

1. Reproduce the behavior against the current supported branch or release candidate.
2. Separate direct observation from interpretation.
3. State the responsibility boundary affected: authority, execution, external effect, evidence, recovery/resume, Human Gate, or provenance.
4. Include the smallest test or example that demonstrates the issue when practical.
5. Do not treat a successful formal proof, unit test, transport receipt, or signed artifact as evidence outside its declared scope.

## Pull requests

A change should normally include:

- a focused explanation of the problem and intended outcome;
- regression tests for changed executable behavior;
- EN/JA documentation updates when public behavior or claims change;
- an explicit compatibility note for persisted state or public APIs;
- an explicit proof ceiling when Lean/formal artifacts are changed;
- no credentials, private research material, or internal-only evidence.

Changes that alter authority, Human Gate semantics, external-effect handling, public claims, persistence compatibility, or release behavior require stronger review than ordinary refactoring.

## Security reports

Do not disclose exploitable security details in a public issue before reading `SECURITY.md`.

## Evidence discipline

RPOS follows a simple rule: claims must remain proportional to evidence. A contribution may improve implementation evidence without proving deployment safety, legal validity, organizational responsibility, or real-world external effects.
