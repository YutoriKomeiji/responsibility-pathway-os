# RPOS Evaluation Evidence Import v0.1

Status: Private RPP Engineering Profile / Japan-first

## Purpose

Define a bounded serialized import format for external AI evaluation evidence so Japanese safety/capability evaluation outputs can be attached to an RPOS operation without importing arbitrary logs, secrets, or evaluator-specific state into the normative core.

## CLI

```text
rpos --db <database> record-evaluation-json <operation_id> <path> --actor <evidence_producer>
```

This command records evidence only. It MUST NOT approve, authorize, dispatch, reconcile, repair, resume, verify an external effect, or complete an operation.

## Strict JSON schema v0.1

Required fields:

- `evidence_id`;
- `evidence_class`;
- `source_system`;
- `source_reference`;
- `source_revision`;
- `evaluation_scope`;
- `result_summary`.

Optional fields:

- `artifact_digest`.

No other fields are accepted in v0.1.

Supported evidence classes:

- `safety_evaluation`;
- `capability_evaluation`.

## Provenance rule

Serialized imports require `source_revision` even though programmatic in-process construction may omit it for backwards-compatible private-alpha use.

The revision identifies the evaluator configuration, source revision, release, commit, or other stable revision token used by the evidence producer. RPOS does not infer what the token means; the producer must use a value appropriate to the upstream evaluation system.

`artifact_digest`, when supplied, identifies a bounded external artifact. RPOS v0.1 records the digest but does not fetch, trust, or independently validate the referenced artifact.

## Bounded-ingestion rule

The strict allowlist intentionally excludes:

- credentials;
- API keys or tokens;
- raw model prompts/responses;
- arbitrary evaluator logs;
- large result blobs;
- remote authorization state;
- external-system completion state.

Detailed artifacts remain external and are referenced through bounded provenance fields.

## Japan reference usage

For Japan AISI safety-evaluation workflows, import a bounded result summary and the relevant evaluation-source revision as `safety_evaluation` evidence.

For Japanese-language model evaluation workflows such as LLM-jp evaluation, import a bounded result summary and the relevant evaluation-source revision as `capability_evaluation` evidence.

These mappings are interoperability/evidence patterns only. They do not imply endorsement, official certification, evaluator correctness, or direct compatibility with every upstream output format.

## Error behavior

The importer fails closed when:

- a required field is missing;
- an unexpected field is present;
- the evidence class is unsupported;
- a required textual value is empty;
- supplied optional provenance is empty.

A failed import must not append an evaluation-evidence event.

## Not Proven

Import success proves only that the bounded record satisfied the RPOS v0.1 import schema and was durably attached to the operation event history. It does not prove the evaluation was executed correctly, the source artifact is authentic, the evaluated model is safe, the operation is authorized, or any external effect occurred.
