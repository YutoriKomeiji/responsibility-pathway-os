# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Protocol

from .models import AdapterResult, ReceiptStatus, ReconciliationResult, ReconciliationStatus


class OperationAdapter(Protocol):
    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        ...


class ReconciliationObserver(Protocol):
    def observe(
        self,
        *,
        operation_id: str,
        latest_attempt: dict[str, Any] | None,
    ) -> ReconciliationResult:
        ...


class JsonlFileOperationAdapter:
    """Bounded external-effect adapter for an append-only JSONL sink.

    The sink is intentionally outside the RPOS SQLite store. A successful append
    is only a receipt: this adapter does not claim that the external effect has
    been independently verified. Use :class:`JsonlFileReconciliationObserver`
    for the readback step.
    """

    def __init__(self, path: str | Path, payload: Mapping[str, Any] | None = None) -> None:
        self.path = Path(path)
        self.payload = dict(payload or {})

    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        existing = _find_jsonl_record(self.path, operation_id, idempotency_key)
        if existing is not None:
            return AdapterResult(
                receipt_status=ReceiptStatus.SUCCEEDED,
                receipt={"recorded": True, "duplicate_prevented": True, "path": str(self.path)},
                readback_verified=None,
                readback=None,
                reason="existing_idempotent_effect",
            )

        record = {
            "operation_id": operation_id,
            "attempt_id": attempt_id,
            "idempotency_key": idempotency_key,
            "payload": self.payload,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()

        return AdapterResult(
            receipt_status=ReceiptStatus.SUCCEEDED,
            receipt={"recorded": True, "duplicate_prevented": False, "path": str(self.path)},
            readback_verified=None,
            readback=None,
            reason="external_receipt_requires_independent_readback",
        )


class JsonlFileReconciliationObserver:
    """Observation-only readback for ``JsonlFileOperationAdapter`` effects."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def observe(
        self,
        *,
        operation_id: str,
        latest_attempt: dict[str, Any] | None,
    ) -> ReconciliationResult:
        if latest_attempt is None:
            return ReconciliationResult(
                status=ReconciliationStatus.UNRESOLVED,
                evidence={},
                reason="no_execution_attempt_available",
            )
        idempotency_key = str(latest_attempt.get("idempotency_key") or "")
        if not idempotency_key:
            return ReconciliationResult(
                status=ReconciliationStatus.UNRESOLVED,
                evidence={},
                reason="attempt_missing_idempotency_key",
            )

        record = _find_jsonl_record(self.path, operation_id, idempotency_key)
        if record is not None:
            return ReconciliationResult(
                status=ReconciliationStatus.VERIFIED_APPLIED,
                evidence={
                    "sink": str(self.path),
                    "operation_id": operation_id,
                    "idempotency_key": idempotency_key,
                    "record": record,
                },
                reason="jsonl_effect_readback_verified",
            )

        return ReconciliationResult(
            status=ReconciliationStatus.VERIFIED_NOT_APPLIED,
            evidence={
                "sink": str(self.path),
                "operation_id": operation_id,
                "idempotency_key": idempotency_key,
            },
            reason="jsonl_effect_absent_on_authoritative_readback",
        )


def _find_jsonl_record(path: Path, operation_id: str, idempotency_key: str) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL record at line {line_number}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"JSONL record at line {line_number} is not an object")
            if record.get("operation_id") == operation_id and record.get("idempotency_key") == idempotency_key:
                return record
    return None
