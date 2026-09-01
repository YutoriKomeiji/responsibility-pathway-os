# RPOS Support

RPOS is actively developed and may be used within documented boundaries. The current `0.1.x` alpha label describes release maturity and change expectations; it does not mean `do not use`.

Support is best-effort and focused on reproducible engineering issues, field integrations, adversarial cases, and product-quality feedback.

## Good support requests

Please include:

- RPOS version and installation method;
- Python version and operating system;
- the command or API path used;
- expected responsibility state and observed responsibility state;
- whether any external effect may already have occurred;
- the smallest reproducible input that does not contain secrets or protected data;
- whether the issue concerns correctness, usability, performance, compatibility, security, or integration burden.

If execution may have occurred but the external effect is uncertain, do not retry merely to test the report. Preserve the state and evidence first.

## Current use posture

The documented runtime, persistence/restart continuity, Human Gate, reconciliation, repair/resume, evidence/provenance surfaces, and bounded formal artifacts are intended to be tried in real bounded integrations.

RPOS does not itself provide every production concern. Deployment-specific authentication, authorization, credential isolation, network/TLS policy, tenant isolation, bypass prevention, and correctness of arbitrary external systems remain integrator-owned unless a future RPOS surface explicitly implements them.

That means `not provided by RPOS`, not `all real use is forbidden`.

## Supported questions and field reports

Useful reports include installation, CLI/API behavior, documented examples, persistence/restart behavior, Human Gate transitions, reconciliation, repair/resume, evidence/provenance surfaces, bounded formal artifacts, deployment friction, adapter behavior, failure recovery, and cases where the state model is too heavy, too weak, or unclear.

Real environment reports extend evidence for those environments. They do not automatically create a universal production-readiness, legal, compliance, or third-party-system correctness claim.

## Compatibility

The `0.x` line may evolve and may contain breaking changes. `0.x` means evolving public contract surface, not evaluation-only software. Breaking changes should be versioned and accompanied by migration guidance where practical.

## Security

For suspected vulnerabilities, follow `SECURITY.md` rather than opening a public exploit report.

## Service level

RPOS is best-effort open-source software without a guaranteed response or resolution time.
