# RPOS CLI Control Surface Detailed Design v0.1

Status: Private RPP Detailed Design Candidate

## Objective

Expose a small command-line control surface over the current `RposService` while preserving the service as the single authority for state transitions.

## Commands

- `boot`
- `unresolved`
- `inspect OPERATION_ID`
- `propose-json PATH`
- `approve OPERATION_ID --actor ACTOR`
- `deny OPERATION_ID --actor ACTOR --reason TEXT`
- `prepare-repair OPERATION_ID --actor ACTOR --summary TEXT`
- `resume OPERATION_ID --actor ACTOR`

Global option:
- `--db PATH` selects the SQLite database. Default: `rpos.db`.

## Output contract

Successful commands emit one JSON object to stdout. Enum values are serialized as strings. Human Return information is included when present.

Errors caused by invalid state, invalid input, missing files, or insufficient authority emit a compact JSON error object to stderr and return a nonzero exit code.

## Mutation boundary

Read commands (`boot`, `unresolved`, `inspect`) must not mutate state.

Mutation commands invoke only public `RposService` methods. The CLI must not call `_transition` or access SQLite internals directly.

No command in this slice dispatches an external operation, performs automatic recovery, or constructs an adapter.

## Proposal input

`propose-json` accepts a UTF-8 JSON file whose top-level object maps directly to `OperationDefinition.from_dict`.

This avoids a large unstable flag surface while the private alpha data model is still moving.

## Exit behavior

- `0`: command succeeded;
- `2`: user/input error, missing resource, invalid state, or permission failure;
- unexpected internal exceptions may also return `2` in this private slice but must be represented as a bounded error type rather than a Python traceback by default.

## Tier-A verification

1. boot emits JSON and does not mutate;
2. proposal from JSON enters expected state;
3. inspect preserves Human Return fields;
4. wrong approval actor returns nonzero without transition;
5. repair/resume commands enforce service authority;
6. read commands do not call recovery or dispatch;
7. JSON serialization is stable for enums/dataclasses used in this slice.

GitHub Actions are not required for this unit.
