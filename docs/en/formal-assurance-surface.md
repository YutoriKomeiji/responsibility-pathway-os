<!-- RPOS-DOC-ID: RPOS-FORMAL-ASSURANCE-001 -->
<!-- RPOS-DOC-LANG: en -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../ja/formal-assurance-surface.md -->

# RPOS Formal Assurance Surface

## Purpose

RPOS uses Lean 4 as a **public assurance/evidence plane**, not merely as a source-development check and never as runtime authority.

The product surface connects:

`operational risk -> bounded Lean theorem -> machine-check status -> executable runtime test -> proof ceiling -> exact source commit`

This lets an evaluator see both what is machine-checked and what remains outside the theorem's scope.

## Source of truth

- `formal/assurance-catalog.json` defines the user-visible risk/theorem/runtime-test crosswalk.
- `tools/build_formal_assurance_manifest.py` validates every theorem and pytest selector against the exact source tree and records source SHA-256 digests.
- `formal/lean/lean-toolchain` pins the Lean toolchain.
- `site/assurance.html` renders the deployed evidence.

The generated manifest schema is `rpos.formal-assurance.manifest.v0.1`.

## Machine-check route

A manifest may only advertise `lean.machine_checked = true` after `cd formal/lean && lake build` succeeds for the same Git commit. GitHub Pages performs that build before generating the public `formal-assurance.json`. The release-candidate workflow performs the same sequence and includes `formal-assurance.json` in the source-bound release evidence and release hash bundle.

The manifest records:

- exact `source_commit`;
- pinned Lean toolchain;
- catalog SHA-256;
- each theorem source SHA-256;
- each referenced runtime-test source SHA-256;
- model scope and per-assertion proof ceiling;
- evidence role `public_assurance_not_runtime_authority`.

## Evidence separation

Formal proof evidence does not impersonate executable implementation evidence or operational effect evidence. A Lean theorem cannot:

- authorize an operation;
- approve a Human Gate;
- establish that an arbitrary external effect occurred;
- establish the truth or sufficiency of runtime evidence;
- transfer legal, organizational, or operational responsibility.

Those boundaries remain explicit even when the theorem is machine-checked.

## Promotion path

The Public Alpha starts with high-value operational invariants whose meaning is readable without advanced theorem-proving knowledge. Future promotion may add temporal/trace properties and implementation-to-model conformance evidence. An implementation-wide formal-conformance claim remains evidence-limited until an explicit refinement/conformance relation and reproducible conformance evidence exist.
