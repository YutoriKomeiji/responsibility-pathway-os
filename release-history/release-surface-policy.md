# RPOS release-surface policy

Owner: Linear DAN-111

Status: active for `0.1.0a3` and later unless explicitly superseded.

## Purpose

RPOS uses two distinct public release surfaces:

1. **GitHub prerelease / tag** — binds the public release identity to a specific source revision and carries human-readable release notes / source provenance.
2. **PyPI publication** — distributes the verified Python wheel and source distribution.

The two surfaces are related but not equivalent.

```text
github_prerelease != pypi_published
source_release_identity != distribution_publication
```

Creating a GitHub prerelease does not prove that the package is available from PyPI. Publishing to PyPI does not by itself close the release transition.

This policy aligns RPOS with the established RPR public-alpha pattern, where alpha versions are represented as GitHub prereleases and package distributions are published separately.

## Required order for RPOS 0.1.0a3

1. Freeze the exact candidate source revision on `main`.
2. Run the release-candidate workflow with `expected_version=0.1.0a3` and `publish=false` from that exact revision.
3. Verify tests, platform matrix, Lean assurance, wheel/sdist metadata, SBOM, export manifest, and release hashes all bind to the same exact source revision.
4. Obtain the explicit Human Gate for the new public release surfaces.
5. Create tag `v0.1.0a3` at the validated exact source revision.
6. Create GitHub prerelease `RPOS v0.1.0a3` from that exact tag.
7. Verify the GitHub prerelease readback: tag, target/source identity, prerelease flag, and release notes.
8. Run the existing RPOS release workflow with `expected_version=0.1.0a3` and `publish=true` from the validated source line.
9. Read PyPI back independently and verify the published version, filenames, hashes, and Trusted Publisher provenance.
10. Only after successful PyPI readback, promote repository public state (`publication_state`, `latest_published_version`, README/version surfaces, CHANGELOG publication facts).
11. Reconcile GitHub, PyPI, repository metadata, documentation, and article/public surfaces before declaring the transition closed.

## Tag and prerelease requirements

For `0.1.0a3`:

- tag: `v0.1.0a3`
- GitHub release name: `RPOS v0.1.0a3`
- GitHub release type: **prerelease**
- target: the exact validated `main` commit, not a moving branch reference at decision time
- package identity: `responsibility-pathway-os==0.1.0a3`

The release notes must preserve the alpha / non-production boundaries and state that GitHub prerelease publication does not itself imply PyPI availability until public readback confirms it.

## Human Gates

The following are external publication actions and require explicit Master approval:

- creating/publishing the Git tag if it establishes the public release identity;
- publishing the GitHub prerelease;
- publishing distributions to PyPI;
- publishing an external article or announcement that states the release is public.

Internal branch/PR work, tests, release-note drafting, `publish=false` validation, and other reversible preparation remain permitted under DAN-111.

## Release-boundary invariants

Preserve throughout the transition:

```text
release_candidate != released_distribution
github_prerelease != pypi_published
validation_success != publication_authority
publication_success != transition_closure
route_selection != authority_grant
```

A tag or GitHub prerelease does not create production readiness, legal/compliance certification, organizational Authority, universal safety, third-party correctness, or implementation-wide formal correctness.

## Post-release closure

The version transition is not closed until all public surfaces agree on the same release facts and the public readback has been completed.

At minimum reconcile:

- exact source commit / tag;
- GitHub prerelease state;
- PyPI version and artifact hashes;
- `product-status.json`;
- README EN/JA installation/version guidance;
- CHANGELOG publication record;
- release-history record;
- product/site/article surfaces that name the current release.
