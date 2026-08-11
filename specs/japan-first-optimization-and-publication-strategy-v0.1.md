# RPOS Japan-First Optimization and Publication Strategy v0.1

Status: Private RPP Product / Publication Strategy

## Priority order

1. Japan optimization first.
2. International-trend optimization second.

RPOS should first fit Japanese public-sector, enterprise, governance, accountability, documentation, language, and operational expectations before optimizing for global regulatory or market framing.

## Japan-first evidence inputs

Primary evidence classes:

- Japanese official AI/governance guidelines and statutes;
- Digital Agency Government AI "Gennai" public materials and OSS;
- Japanese public-sector procurement, governance, audit, cybersecurity, and accountability practices;
- public Japanese AI products, agent platforms, governance tools, assurance products, workflow systems, and OSS;
- Japanese enterprise operational conventions where observable;
- RPE/RPR field experience and RPOS implementation evidence.

Current confirmed high-priority official inputs include:

- AI Guidelines for Business Ver.1.2 (METI / AISI-related governance process);
- Digital Agency Government AI "Gennai", including its large-scale government deployment and OSS publication;
- guidance for cyber-infrastructure providers and related software-supply-chain accountability materials.

These are requirements/evidence inputs, not authority shortcuts. RPOS must explain exactly which requirement is derived from which source and what RPOS does technically in response.

## Publication method — evidence-backed problem/solution argument

RPOS may use a strong public communication structure similar to common product/advocacy publishing patterns:

```text
recognized authority / standard / public system
        ↓
observable requirement, limitation, unresolved boundary, or engineering gap
        ↓
why that gap matters technically or operationally
        ↓
what mechanism is needed
        ↓
what RPOS implements
        ↓
what evidence demonstrates that implementation
        ↓
what remains Not Proven / operator-owned / environment-owned
        ↓
why we recommend using RPOS for the bounded problem
```

The point is not to borrow another organization's claims. The point is to use public standards and artifacts as an explicit argumentative starting point while preserving full technical causality.

## Prohibited rhetorical shortcut

Do not publish:

```text
Authority X says important thing Y.
Therefore RPOS.
```

Do publish:

```text
Authority X defines/expects Y.
In an executable system Y implies engineering conditions A/B/C.
Without A/B/C, failure modes D/E remain possible.
RPOS implements A/B/C using mechanism M/N/P.
Tests / conformance / formal model / operational evidence support bounded claims Q/R.
Therefore RPOS is recommended where those bounded requirements apply.
```

Every material connection should answer:

- Why does the cited requirement matter?
- Why does it create an engineering need?
- Why is the proposed mechanism responsive to that need?
- What evidence shows RPOS actually implements the mechanism?
- What does the evidence not establish?

## Responsibility-preserving publication model

Public claims must not allow responsibility to disappear into collective language, nor assign all responsibility to the project owner.

For each consequential public claim, identify where practical:

- **Claim Owner** — who/what project surface asserts the claim;
- **Evidence Producer** — test, formal proof, implementation artifact, operational readback, external source;
- **Review Role** — who reviewed wording/scope internally;
- **Operational Owner** — deployer/operator responsibility after adoption;
- **Dependency Owner** — external service/platform responsibilities that RPOS cannot control;
- **Residual Owner** — who must act if evidence is incomplete, environment differs, or operation remains unresolved;
- **Human Return Point** — where a human decision is explicitly required.

The human project owner remains final publication authority, but publication wording should not imply that every downstream operational, organizational, legal, security, or external-service responsibility personally transfers to that individual.

## Claim grammar

Prefer claims in this form:

> Because [source/observed system] establishes or exposes [bounded requirement/problem], a system performing [operation class] needs [technical property]. RPOS implements that property through [mechanism]. We demonstrate the implementation with [runtime/test/conformance/proof/readback]. This does not establish [explicit limits]. We therefore recommend RPOS for [bounded use].

Avoid vague superiority claims unless comparative evidence supports them.

## Japan product fit priorities

RPOS design should prioritize:

- Japanese-language operational clarity;
- explicit Human Gate / responsible-person handoff;
- audit/explanation artifacts usable by organizations, not only developers;
- conservative handling of UNKNOWN / PARTIAL / unresolved external effects;
- deployer-visible authority and permission boundaries;
- public-sector and enterprise accountability chains;
- software-supply-chain and external-adapter responsibility boundaries;
- documentation suitable for Japanese procurement, internal control, audit, and management review;
- simple local/controlled deployment before assuming hyperscale cloud architecture;
- interoperability with Japanese public/enterprise AI environments where technically and legally appropriate.

## Gennai study direction

Digital Agency Government AI "Gennai" is a particularly important Japan-first reference because it is a real government AI environment, has large-scale cross-ministry deployment, and has an OSS publication path.

RPOS should study, without copying protected expression or blindly mirroring architecture:

- deployment/control-plane architecture exposed publicly;
- model/application selection and governance boundaries;
- authentication/authorization patterns;
- logging and audit surfaces;
- application/plugin/tool boundaries;
- government-data handling boundaries;
- operator/admin responsibility;
- OSS-to-government-deployment differences;
- extension points where a responsibility-control runtime could complement rather than duplicate Gennai.

## International optimization — second pass

After the Japan profile is stable, map RPOS to international trends such as:

- NIST AI RMF and related profiles;
- ISO/IEC AI management/governance/security standards where accessible;
- EU AI Act implementation guidance and codes of practice;
- agentic AI governance / tool-execution control patterns;
- software supply-chain assurance and secure-by-design expectations;
- provenance, auditability, authorization, recovery, and human-oversight practices.

International mapping must remain a translation/conformance layer over the RPOS core, not replace the Japan-first design with a lowest-common-denominator global vocabulary.

## Competitive-publication boundary

RPOS may publicly identify weaknesses, missing evidence, scope limits, or unresolved engineering needs in public standards/products/repositories when factually supported.

The publication should then show RPOS's response, but must not:

- invent a deficiency merely to create demand;
- imply endorsement by an authority/source;
- hide the reasoning bridge from source to product;
- collapse formal proof into deployment assurance;
- omit material limitations from high-salience presentation;
- shift every residual risk onto the project owner or every operational risk onto the user.

## Immediate implementation consequences

This strategy should feed upcoming work:

1. create a Japan requirements/evidence matrix;
2. inspect Gennai OSS/public architecture;
3. map AI Guidelines for Business 1.2 requirements to RPOS mechanisms/gaps;
4. map Japanese cybersecurity/software-supply-chain guidance to adapter/runtime boundaries;
5. define RPOS public claim/evidence metadata;
6. add Claim Owner / Evidence / Not-Proven / Residual Owner metadata to release documentation;
7. only then create international mapping documents.
