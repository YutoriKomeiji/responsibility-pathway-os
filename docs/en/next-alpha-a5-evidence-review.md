# RPOS 0.1.0a5 — candidate evidence review (not a release)

Status: REVIEW / UNRELEASED. The last published PyPI package remains `0.1.0a4`.

## New current-main code under review
- `src/rpos/route_eligibility.py` implements receiver eligibility based on independently supplied facts; unknown or false checks cannot turn a route into permission. Its caller still owns the truth of external authorization, delegation and evidence.
- `src/rpos/route_assessment_history.py` adds scoped assessment history; confirm persistence, interface and retention before claiming durable coverage.
- `src/rpos/rpr_route_crosswalk.py` defines a bounded RPR/RPOS route mapping; a crosswalk does not mean interoperability in every external deployment.
- Matching tests exist; this candidate adds regressions for mixed unknown/false inputs, blank evidence basis and expired evidence boundary.

## Positive statement candidates — promote only with exact-head checks
RPOS has a concrete Python/SQLite responsibility state runtime with deliberate distinctions for unknown external effect, readback, repair, resume, Human Gate and typed routes. Current main contains additional eligibility/crosswalk/history implementation beyond the published a4 line. Test the exact source/package before describing those new modules as shipped a5 functionality.

## Material boundary
An assessed route does not create the receiving party's authority. Lean 4 machine-checked statements apply to declared model-level invariants, not the complete Python runtime or arbitrary external systems. Production and independent customer environment validation are not established by local fixtures.

## Release-candidate closure checklist
1. Confirm route eligibility and crosswalk behavior, including receiver identity, evidence expiry, residual owner and malformed data.
2. Review outstanding PR #45 (post-restart unknown-effect/handoff cases) and PR #40 (reader entry) before conflicting edits.
3. Validate API/CLI, SQLite restart/repair/reconciliation, wheel+sdist clean install, exact-head Lean 4 model/catalog manifest, SBOM and public site.
4. Reconcile EN/JA README, product-status, `PYPI_README.md`, `pyproject.toml`, release workflow `expected_version` and current-vs-published lifecycle checks in one coherent candidate step.
5. Run release-candidate workflow with `publish=false` and check terminal result/readback. Do **not** create release/tag or upload to PyPI without a separate Human Gate.
