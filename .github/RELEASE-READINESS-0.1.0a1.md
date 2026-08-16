# RPOS 0.1.0a1 Publishable Freeze Gate

Status: `PRE_PUBLISH_VALIDATION`

Target: `responsibility-pathway-os==0.1.0a1`

This record defines the boundary between an engineering-complete public-alpha candidate and an externally published release. It does not authorize repository visibility changes, GitHub Release creation, tags, PyPI upload, Pages/demo publication, or announcement.

## Required before PUBLISHABLE_FREEZE

- [x] Package identity and version are declared in `pyproject.toml`.
- [x] README EN/JA version markers and install examples are checked against the package version.
- [x] Wheel and sdist are built from one candidate checkout.
- [x] Rendered wheel/sdist metadata are checked against the requested release identity.
- [x] `twine check` is part of the release-candidate route.
- [x] Declared Python 3.11 and 3.12 compatibility are exercised in the release-candidate route.
- [x] Verified distributions are transferred to the publish job as one immutable workflow artifact instead of being rebuilt in the publish job.
- [x] PyPI publication is isolated in `.github/workflows/release.yml` and requires an explicit `publish=true` workflow input.
- [x] The publish job uses OIDC Trusted Publishing (`id-token: write`) and does not require a long-lived PyPI API token.
- [ ] Exact candidate branch/head passes the existing standalone verification workflow after these release-gate changes.
- [ ] Exact candidate branch/head passes `RPOS release candidate` with `publish=false`.
- [ ] GitHub `pypi` environment exists and has the intended protection rules.
- [ ] PyPI Trusted Publisher (or pending publisher for a first release) is configured for owner `YutoriKomeiji`, repository `responsibility-pathway-os`, workflow `release.yml`, environment `pypi`.
- [ ] Final public-surface readback confirms no private research, credentials, unsupported production claims, or stale version text crossed the release boundary.

## Human Gate

The following remain publication actions and are intentionally outside this preparation change:

- changing repository visibility;
- creating a release tag or GitHub Release;
- running `release.yml` with `publish=true`;
- first upload to PyPI;
- external announcement.

`publish=false` is validation-only. `publish=true` is a publication operation and requires explicit human authorization at execution time.

## Freeze rule

Once every pre-publication checkbox above is green, record the exact Git commit as `PUBLISHABLE_FREEZE`. Any source, package metadata, release-workflow, README, test, formal-model, or public-claim change after that commit invalidates the freeze until the release checks are rerun on the new exact head.

A newly imagined feature, edge case, or research slice does not invalidate the freeze by itself. Reopen only for a material release defect, failed validation, changed product outcome, material upstream release dependency, or explicit redesign decision.
