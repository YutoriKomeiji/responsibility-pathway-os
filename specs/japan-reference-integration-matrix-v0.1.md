# RPOS Japan Reference Integration Matrix v0.1

Status: Private RPP Engineering Profile / Japan-first

## Purpose

Define how selected Japanese public AI engineering references connect to RPOS without turning those references into implicit dependencies, endorsements, compliance claims, or substitutes for RPOS authority and operational verification.

The initial reference set covers three distinct social/technical boundaries:

1. Government AI execution interoperability;
2. AI safety evaluation evidence;
3. Japanese-language model capability evaluation evidence.

Forked repositories are retained as engineering reference snapshots. RPOS normative behavior MUST remain independently defined and MUST NOT depend on a fork merely existing.

## Integration matrix

| Reference | Primary observed role | RPOS connection | Evidence class | Must not imply |
| --- | --- | --- | --- | --- |
| Government AI Gennai public repositories | Government AI user/application execution boundary and external application lifecycle | bounded operation adapter and reconciliation observer | execution receipt / remote lifecycle evidence | RPOS authorization, verified real-world effect, endorsement, deployed compatibility |
| Japan AISI `aisev` | AI safety evaluation support, including quantitative/qualitative evaluation and automated red teaming | import bounded evaluation result/provenance as review evidence | `safety_evaluation` | Human Gate approval, operational effect verification, official certification or guarantee |
| `llm-jp/llm-jp-eval` | automated evaluation across Japanese LLM datasets | import bounded evaluation result/provenance as review evidence | `capability_evaluation` | permission to execute consequential operations, safety certification, verified external effect |

## Core separation rule

```text
model capability evaluation
        │
AI safety evaluation
        │
        ▼
RPOS evaluation evidence
        │
        ├── may inform responsible review
        ├── may be retained in event/evidence history
        └── MUST NOT create authority or operational verification

RPOS Human Gate / authority ─────────────── independent
RPOS dispatch receipt ───────────────────── independent
RPOS external-effect readback ───────────── independent
```

An evaluation score, pass/fail label, red-team result, benchmark ranking, or evaluation-system completion status is evidence about the declared evaluation scope only.

It is not, by itself:

- authorization to dispatch an operation;
- proof that an external operation executed;
- proof that a requested real-world effect occurred;
- proof of legal or regulatory compliance;
- proof of general AI safety;
- transfer of responsibility from the declared RPOS authority or residual owner.

## Initial executable boundary

RPOS provides `ExternalEvaluationEvidence` with two initial evidence classes:

- `safety_evaluation`;
- `capability_evaluation`.

The record contains:

- evidence id;
- evidence class;
- source system;
- source reference;
- declared evaluation scope;
- bounded result summary;
- optional artifact digest.

`RposService.record_evaluation_evidence(...)` records the evidence as an event associated with an existing operation. It deliberately performs no state transition.

This makes the following invariant executable:

```text
Evaluation Evidence != Authority
Evaluation Evidence != Dispatch Receipt
Evaluation Evidence != Operational Readback
Evaluation Evidence != RPOS VERIFIED
```

## Japan-first usage direction

### Government / public-sector AI

Use the existing Gennai adapter design to study execution, asynchronous status, restart, reconciliation, and authority separation. Remote application completion remains distinct from verified real-world effect.

### AI safety evaluation

Use safety-evaluation outputs as bounded inputs to Human Gate, audit, procurement, incident review, and release evidence packages. Preserve the evaluator's own scope and non-guarantee conditions.

### Japanese-language capability evaluation

Use capability-evaluation outputs to describe tested model behavior and limitations for Japanese deployment contexts. Capability evidence may affect policy decisions but never grants permission by itself.

## Provenance and fork discipline

Reference forks are for reproducible inspection and bounded interoperability/evidence work.

For each future integration:

1. record upstream identity and relevant revision;
2. identify the minimum observed interface or output contract used;
3. preserve upstream license and attribution requirements;
4. implement RPOS-side contracts independently;
5. avoid copying implementation structures when an interface-level mapping is sufficient;
6. keep external project names out of RPOS product metadata except where factually necessary for neutral interoperability or evidence documentation.

## Next implementation units

1. add a serialized evaluation-evidence import format with strict schema validation;
2. define audit-export representation separating evaluation, authority, execution, and operational evidence;
3. map AI Guidelines for Business expectations to these evidence classes without claiming compliance;
4. implement the bounded Gennai adapter after the current formal/machine-check sequencing gate is resolved;
5. add source-revision and artifact-digest provenance rules suitable for reproducible Japanese evaluation evidence;
6. defer NIST / ISO / EU mappings until the Japan operational profile is stable.

## Not Proven

This profile does not prove compatibility with deployed government systems, correctness of external evaluators, official certification, regulatory compliance, production readiness, or general safety of any evaluated model or RPOS itself.
