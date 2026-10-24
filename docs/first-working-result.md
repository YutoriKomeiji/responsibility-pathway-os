# First working result: durable responsibility state

**Problem:** An automation system needs to preserve the distinction between an approved action, a dispatched action, a verified external effect, and an unresolved effect—even after a restart.

RPOS provides an executable Python/SQLite responsibility-state runtime; no enterprise account is required for its local introductory workflow.

## Try the published CLI

Requirements: Python 3.11+.

```bash
python -m pip install responsibility-pathway-os==0.1.0a4
rpos --db rpos.db boot
```

This creates or initializes a local RPOS operating store. It does not approve real operations or carry out an external mutation.

## See a scenario with observable transitions

From a checkout of the corresponding repository source, the README documents:

```bash
python examples/production_grade_demos/run_demo.py
```

The integration suite uses deterministic localhost fixtures. It covers bounded examples such as supplier payments, deployment repair and privileged-access denial; it is **not** a live payment processor or IAM evaluation. Match any run to the applicable source revision and record its actual output.

## What to inspect

- Authorization, dispatch, effect observation and verification are different states.
- `EFFECT_UNKNOWN` is retained instead of becoming automatic success or a blind retry.
- Repair readiness does not itself grant resume Authority.
- Selected Lean 4 invariants concern modeled properties, not blanket proof of deployed Python behavior.

See the [public README](../README.md) for component scope, current released version and the formal-assurance references.

## Use and extend it

RPOS is published under the [MIT license](../LICENSE): run it, fork it, adapt it and maintain your own changes if that fits your needs. [CONTRIBUTING](../CONTRIBUTING.md) welcomes reproductions, extension ideas, counterexamples and documentation fixes; use [Issues](https://github.com/YutoriKomeiji/responsibility-pathway-os/issues) for non-sensitive reports and [SECURITY](../SECURITY.md) for exploitable weaknesses.

Real service integration, deployment portability and environmental assumptions remain open to third-party evidence. Supply reproducible setup, expected/observed output and relevant version information. An absence of maintainer-accessible enterprise infrastructure is a request for collaboration, not a blanket assertion that the released local functionality is unusable.
