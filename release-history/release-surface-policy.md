# RPOS release-surface policy

Owner: Linear DAN-111

Status: active for `0.1.0a3` and later unless explicitly superseded.

## Core release rule

A release version is established **before** external publication.

During release preparation, every active/current-facing source surface that names the release identity MUST already point to the **next release version**. Publication status and release identity are separate state dimensions.

```text
candidate_version_identity != publication_state
next_version_before_publish == package_version == active_document_version == assurance_product_version
pypi_publish == final_distribution_action
```

Therefore, when preparing version `X` while version `Y` is still the latest public release:

- `pyproject.toml` uses `X`;
- `product-status.json.version` uses `X`;
- README EN/JA document-version markers and install examples use `X`;
- GitHub Pages source EN/JA uses `X`;
- active current-scope / claim-boundary / routing documents use `X`;
- `formal/assurance-catalog.json.product_version` uses `X`;
- package long-description metadata uses `X`;
- `latest_published_version` may still remain `Y` until public readback proves `X` exists;
- candidate wording MUST say release candidate / not yet published and MUST NOT claim that `X` is already the current public release.

PyPI publication is not the operation that creates the version identity. It is the final package-distribution publication step for an identity already made internally consistent and validated.

## Public release surfaces

RPOS uses two distinct external release surfaces:

1. **GitHub prerelease / tag** — binds the public release identity to a specific source revision and carries human-readable release notes / source provenance.
2. **PyPI publication** — distributes the already-verified Python wheel and source distribution.

The two surfaces are related but not equivalent.

```text
github_prerelease != pypi_published
source_release_identity != distribution_publication
validation_success != publication_authority
publication_success != transition_closure
```

## Required release order

For every release version `X`:

1. **Start release preparation.** Select `X` and move package identity plus all active/current-facing document, site, assurance, and package-description version markers to `X`.
2. Keep `publication_state=not_published` and retain the previous public version only as historical/public-readback state where needed. Do not use the previous public version as the active document identity.
3. Mark candidate-facing wording explicitly as release candidate / not yet published. No active surface may claim `X` is already published.
4. Run repository tests that verify version coherence across package metadata, README EN/JA, Pages source, active docs, Formal Assurance catalog/manifest, product status, and package long description.
5. Freeze the exact candidate source revision on `main`.
6. Run the release workflow with `expected_version=X` and `publish=false` from that exact revision.
7. Inspect the generated wheel and sdist, including rendered `METADATA` / `PKG-INFO`, and verify they identify `X`.
8. Verify tests, platform matrix, Lean assurance, SBOM, public-export manifest, release hashes, and Formal Assurance manifest all bind to the same exact source revision and version `X`.
9. Obtain the explicit Human Gate for external release identity.
10. Create tag `vX` at the validated exact source revision and create GitHub prerelease `RPOS vX`.
11. Read GitHub prerelease back: tag, target/source identity, prerelease flag, and release notes.
12. Obtain/confirm the PyPI Human Gate, then run the release workflow with `expected_version=X` and `publish=true`.
13. Read PyPI back independently and verify version, filenames, hashes, Trusted Publisher provenance, and rendered package page / Quick Start.
14. After public readback, change only publication-state facts: e.g. `publication_state=pypi_published`, `latest_published_version=X`, candidate wording -> current published wording.
15. Re-run current-surface reconciliation and Pages deployment, then read public surfaces back.
16. Preserve historical release evidence unchanged and close the transition only when all current surfaces agree.

## Pre-publication fail-closed requirements

Release validation MUST fail if any of the following is true:

- an active/current-facing surface still identifies the previous release as its own document/product version;
- package metadata says `X` while README, Pages source, active docs, or Formal Assurance catalog identifies an older version;
- wheel/sdist rendered long description contains an old install target;
- Formal Assurance manifest `product_version` differs from `pyproject.toml`;
- candidate wording claims `X` is already published;
- `publish=true` is requested after repository state already says the same version is published;
- exact-head artifact evidence cannot be bound to the validated source revision.

Historical records, changelog history, regression fixtures, and explicit descriptions such as “X preserves behavior from Y” are allowed to retain old version identifiers.

## Post-publication closure

The version transition is not closed merely because PyPI returned success.

At minimum reconcile and read back:

- exact source commit / tag;
- GitHub prerelease state;
- PyPI version, rendered description, filenames, hashes, and provenance;
- `product-status.json`;
- README EN/JA;
- GitHub Pages EN/JA;
- active current-scope / claim-boundary / routing documents;
- `formal/assurance-catalog.json` and generated Formal Assurance manifest;
- package long description;
- CHANGELOG publication record;
- product/demo surfaces that name the current release;
- related article/public surfaces when they state the current release.

## Human Gates

The following remain external publication actions and require explicit Master approval:

- publishing the Git tag / GitHub prerelease;
- publishing distributions to PyPI;
- publishing an external article or announcement that states the release is public.

Internal branch/PR work, tests, release-note drafting, `publish=false` validation, metadata preparation, version-coherence repair, and other reversible preparation remain permitted under DAN-111.

## Responsibility boundary

A version transition does not create production readiness, legal/compliance certification, organizational Authority, universal safety, third-party correctness, or implementation-wide formal correctness.
