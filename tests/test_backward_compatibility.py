# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from rpos import AdmissionDecision, OperationState
from rpos.storage import SQLiteRposStore


def _create_legacy_alpha_database(path: Path) -> None:
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE operations (
            operation_id TEXT PRIMARY KEY,
            definition_json TEXT NOT NULL,
            state TEXT NOT NULL,
            admission_decision TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE attempts (
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
        CREATE TABLE events (
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

    # Earlier alpha payloads predate explicit resume_authority and may omit
    # optional gate/verification fields. The current reader must retain their
    # meaning rather than forcing destructive migration.
    legacy_definition = {
        "operation_id": "legacy-alpha-001",
        "action_name": "legacy_bounded_operation",
        "requested_by": "legacy_requester",
        "execution_actor": "legacy_executor",
        "approval_authority": None,
        "human_return_point": "legacy-human-return",
        "residual_owner": "legacy-owner",
    }
    connection.execute(
        "INSERT INTO operations(operation_id, definition_json, state, admission_decision, updated_at) VALUES (?, ?, ?, ?, ?)",
        (
            "legacy-alpha-001",
            json.dumps(legacy_definition, sort_keys=True),
            OperationState.PROPOSED.value,
            AdmissionDecision.ALLOW.value,
            "2026-08-08T00:00:00+00:00",
        ),
    )
    connection.commit()
    connection.close()


def test_current_reader_opens_supported_legacy_alpha_state_without_destructive_migration(tmp_path: Path) -> None:
    database = tmp_path / "legacy-alpha.db"
    _create_legacy_alpha_database(database)

    store = SQLiteRposStore(database)
    definition, state, decision = store.get_operation("legacy-alpha-001")

    assert state is OperationState.PROPOSED
    assert decision is AdmissionDecision.ALLOW
    assert definition.operation_id == "legacy-alpha-001"
    assert definition.residual_owner == "legacy-owner"
    assert definition.effective_resume_authority == "legacy-owner"
    assert definition.requires_human_gate is False
    assert definition.verification_required is True


def test_opening_supported_legacy_alpha_state_does_not_rewrite_persisted_definition(tmp_path: Path) -> None:
    database = tmp_path / "legacy-alpha.db"
    _create_legacy_alpha_database(database)

    before = sqlite3.connect(database).execute(
        "SELECT definition_json FROM operations WHERE operation_id = ?",
        ("legacy-alpha-001",),
    ).fetchone()[0]

    store = SQLiteRposStore(database)
    store.get_operation("legacy-alpha-001")

    after = sqlite3.connect(database).execute(
        "SELECT definition_json FROM operations WHERE operation_id = ?",
        ("legacy-alpha-001",),
    ).fetchone()[0]

    assert after == before
