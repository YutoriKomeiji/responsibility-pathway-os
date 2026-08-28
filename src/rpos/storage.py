# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator

from .models import AdmissionDecision, OperationDefinition, OperationState


def _now() -> str:
    return datetime.now(UTC).isoformat()


class SQLiteRposStore:
    def __init__(self, database_path: str | Path = ":memory:") -> None:
        self.database_path = str(database_path)
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        self._transaction_depth = 0
        self._init_schema()

    @contextmanager
    def transaction(self) -> Iterator[None]:
        """Group store mutations into one SQLite transaction.

        Nested store operations participate in the outer transaction. Public
        mutation methods retain their historical auto-commit behaviour when
        called without this context.
        """
        outermost = self._transaction_depth == 0
        if outermost:
            self.connection.execute("BEGIN IMMEDIATE")
        self._transaction_depth += 1
        try:
            yield
        except Exception:
            self._transaction_depth -= 1
            if outermost:
                self.connection.rollback()
            raise
        else:
            self._transaction_depth -= 1
            if outermost:
                self.connection.commit()

    def _commit_if_outermost(self) -> None:
        if self._transaction_depth == 0:
            self.connection.commit()

    def _init_schema(self) -> None:
        self.connection.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS operations (
                operation_id TEXT PRIMARY KEY,
                definition_json TEXT NOT NULL,
                state TEXT NOT NULL,
                admission_decision TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS attempts (
                attempt_id TEXT PRIMARY KEY,
                operation_id TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                dispatch_started INTEGER NOT NULL,
                dispatch_finished INTEGER NOT NULL,
                receipt_status TEXT,
                readback_verified INTEGER,
                result_reason TEXT,
                UNIQUE(operation_id, idempotency_key),
                FOREIGN KEY(operation_id) REFERENCES operations(operation_id)
            );
            CREATE TABLE IF NOT EXISTS events (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                actor TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(operation_id) REFERENCES operations(operation_id)
            );
            """
        )
        self.connection.commit()

    def create_operation(
        self,
        definition: OperationDefinition,
        state: OperationState,
        decision: AdmissionDecision,
    ) -> None:
        self.connection.execute(
            "INSERT INTO operations(operation_id, definition_json, state, admission_decision, updated_at) VALUES (?, ?, ?, ?, ?)",
            (
                definition.operation_id,
                json.dumps(definition.to_dict(), sort_keys=True),
                state.value,
                decision.value,
                _now(),
            ),
        )
        self._commit_if_outermost()

    def get_operation(self, operation_id: str) -> tuple[OperationDefinition, OperationState, AdmissionDecision]:
        row = self.connection.execute(
            "SELECT definition_json, state, admission_decision FROM operations WHERE operation_id = ?",
            (operation_id,),
        ).fetchone()
        if row is None:
            raise KeyError(operation_id)
        return (
            OperationDefinition.from_dict(json.loads(row["definition_json"])),
            OperationState(row["state"]),
            AdmissionDecision(row["admission_decision"]),
        )

    def set_state(self, operation_id: str, state: OperationState) -> None:
        cursor = self.connection.execute(
            "UPDATE operations SET state = ?, updated_at = ? WHERE operation_id = ?",
            (state.value, _now(), operation_id),
        )
        if cursor.rowcount != 1:
            raise KeyError(operation_id)
        self._commit_if_outermost()

    def count_operations(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM operations").fetchone()[0])

    def list_by_states(self, states: set[OperationState]) -> list[str]:
        if not states:
            return []
        placeholders = ",".join("?" for _ in states)
        rows = self.connection.execute(
            f"SELECT operation_id FROM operations WHERE state IN ({placeholders}) ORDER BY operation_id",
            tuple(state.value for state in states),
        ).fetchall()
        return [str(row["operation_id"]) for row in rows]

    def get_attempt_by_idempotency_key(self, operation_id: str, idempotency_key: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT * FROM attempts WHERE operation_id = ? AND idempotency_key = ?",
            (operation_id, idempotency_key),
        ).fetchone()
        return None if row is None else dict(row)

    def begin_attempt(self, operation_id: str, attempt_id: str, idempotency_key: str) -> None:
        self.connection.execute(
            "INSERT INTO attempts(attempt_id, operation_id, idempotency_key, dispatch_started, dispatch_finished) VALUES (?, ?, ?, 1, 0)",
            (attempt_id, operation_id, idempotency_key),
        )
        self._commit_if_outermost()

    def finish_attempt(
        self,
        attempt_id: str,
        *,
        receipt_status: str,
        readback_verified: bool | None,
        result_reason: str | None,
    ) -> None:
        cursor = self.connection.execute(
            "UPDATE attempts SET dispatch_finished = 1, receipt_status = ?, readback_verified = ?, result_reason = ? WHERE attempt_id = ?",
            (
                receipt_status,
                None if readback_verified is None else int(readback_verified),
                result_reason,
                attempt_id,
            ),
        )
        if cursor.rowcount != 1:
            raise KeyError(attempt_id)
        self._commit_if_outermost()

    def latest_attempt(self, operation_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT * FROM attempts WHERE operation_id = ? ORDER BY rowid DESC LIMIT 1",
            (operation_id,),
        ).fetchone()
        return None if row is None else dict(row)

    def dispatching_operations(self) -> list[str]:
        """Return all operations stranded in DISPATCHING.

        A finished attempt with a still-DISPATCHING operation is also ambiguous:
        the external effect may have happened while the result transaction did
        not commit. Recovery must therefore include both finished and unfinished
        attempts and must never redispatch automatically.
        """
        rows = self.connection.execute(
            """
            SELECT DISTINCT o.operation_id
            FROM operations o
            JOIN attempts a ON a.operation_id = o.operation_id
            WHERE o.state = ? AND a.dispatch_started = 1
            ORDER BY o.operation_id
            """,
            (OperationState.DISPATCHING.value,),
        ).fetchall()
        return [str(row["operation_id"]) for row in rows]

    def incomplete_dispatch_operations(self) -> list[str]:
        """Backward-compatible alias for restart recovery candidates."""
        return self.dispatching_operations()

    def record_event(self, operation_id: str, event_type: str, actor: str, payload: dict[str, Any]) -> None:
        self.connection.execute(
            "INSERT INTO events(operation_id, event_type, actor, payload_json, created_at) VALUES (?, ?, ?, ?, ?)",
            (operation_id, event_type, actor, json.dumps(payload, sort_keys=True), _now()),
        )
        self._commit_if_outermost()

    def list_events(self, operation_id: str) -> list[dict[str, Any]]:
        self.get_operation(operation_id)
        rows = self.connection.execute(
            "SELECT seq, operation_id, event_type, actor, payload_json, created_at FROM events WHERE operation_id = ? ORDER BY seq",
            (operation_id,),
        ).fetchall()
        return [
            {
                "seq": int(row["seq"]),
                "operation_id": str(row["operation_id"]),
                "event_type": str(row["event_type"]),
                "actor": str(row["actor"]),
                "payload": json.loads(row["payload_json"]),
                "created_at": str(row["created_at"]),
            }
            for row in rows
        ]
