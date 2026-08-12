# Security Policy

## Supported version

The first public-alpha candidate is `0.1.0a1`. Security fixes may be delivered as later alpha releases. Because the project is pre-1.0, supported-version details may change; release notes must identify any security-relevant compatibility or migration requirement.

## Reporting a vulnerability

Please do **not** publish exploit details, credentials, private evidence, or sensitive reproduction data in a public issue.

Preferred route after the repository becomes public:

1. Use GitHub's private vulnerability-reporting / Security Advisory flow when it is enabled for this repository.
2. Include the affected version/commit, affected responsibility surface, prerequisites, minimal reproduction, observed impact, and whether Authority, Evidence, Human Gate, external-effect verification, repair/resume, persistence, or supply-chain integrity may be affected.
3. If private vulnerability reporting is temporarily unavailable, open only a minimal non-sensitive issue asking the repository owner to establish a private reporting channel. Do not include exploit details in that issue.

Before public transition, use the existing private communication path with the repository owner.

## Security response priorities

RPOS treats the following as high-priority security classes in addition to conventional software vulnerabilities:

- Authority bypass, laundering, stale reuse, or cross-operation replay;
- Human Gate bypass or disappearance;
- Evidence substitution, provenance spoofing, or responsibility-history equivocation;
- Residual Owner / Human Return Point erasure or unauthorized replacement;
- unresolved external effects being converted into completion without verification;
- unsafe redispatch, reconciliation abuse, or repair/resume authority restoration errors;
- secret/credential exposure;
- dependency, build, release, SBOM, artifact-hash, or provenance compromise;
- untrusted plugin/MCP/integration input causing authority or execution-boundary violations.

## Security claim boundary

A green test suite, dependency audit, secret scan, SBOM, hash bundle, or bounded Lean proof is evidence for the checked surface only. It does not establish that RPOS is vulnerability-free, production-ready, certified, compliant with a particular regime, or formally verified as a complete Python/runtime system.

Security limitations should be documented as current scope plus remediation/extension paths where possible, without hiding unresolved material risks.
