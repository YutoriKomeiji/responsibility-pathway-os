# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import argparse
import json
import socket
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote


class EffectStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS effects (
                    kind TEXT NOT NULL,
                    external_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    apply_count INTEGER NOT NULL,
                    PRIMARY KEY (kind, external_id)
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def apply(self, *, kind: str, external_id: str, idempotency_key: str, payload: dict[str, object]) -> tuple[dict[str, object], bool]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT idempotency_key, payload_json, apply_count FROM effects WHERE kind=? AND external_id=?",
                (kind, external_id),
            ).fetchone()
            if row is not None:
                if row[0] != idempotency_key:
                    raise ValueError("external identity already exists with a different idempotency key")
                return {
                    "kind": kind,
                    "external_id": external_id,
                    "idempotency_key": row[0],
                    "payload": json.loads(row[1]),
                    "apply_count": row[2],
                }, False

            conn.execute(
                "INSERT INTO effects(kind, external_id, idempotency_key, payload_json, apply_count) VALUES (?, ?, ?, ?, 1)",
                (kind, external_id, idempotency_key, json.dumps(payload, sort_keys=True)),
            )
            return {
                "kind": kind,
                "external_id": external_id,
                "idempotency_key": idempotency_key,
                "payload": payload,
                "apply_count": 1,
            }, True

    def get(self, *, kind: str, external_id: str) -> dict[str, object] | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT idempotency_key, payload_json, apply_count FROM effects WHERE kind=? AND external_id=?",
                (kind, external_id),
            ).fetchone()
        if row is None:
            return None
        return {
            "kind": kind,
            "external_id": external_id,
            "idempotency_key": row[0],
            "payload": json.loads(row[1]),
            "apply_count": row[2],
        }

    def stats(self) -> dict[str, object]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT kind, external_id, idempotency_key, payload_json, apply_count FROM effects ORDER BY kind, external_id"
            ).fetchall()
        effects = [
            {
                "kind": row[0],
                "external_id": row[1],
                "idempotency_key": row[2],
                "payload": json.loads(row[3]),
                "apply_count": row[4],
            }
            for row in rows
        ]
        return {"effect_count": len(effects), "effects": effects}


class EffectHandler(BaseHTTPRequestHandler):
    server_version = "RPOSDemoExternal/1"

    @property
    def store(self) -> EffectStore:
        return self.server.store  # type: ignore[attr-defined]

    def log_message(self, format: str, *args: object) -> None:
        return

    def _parts(self) -> tuple[str, str] | None:
        path = self.path.split("?", 1)[0]
        parts = [unquote(part) for part in path.split("/") if part]
        if len(parts) == 3 and parts[0] == "effects":
            return parts[1], parts[2]
        return None

    def _json(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        parts = self._parts()
        if parts is None:
            self._json(404, {"error": "not_found"})
            return
        kind, external_id = parts
        mode = self.headers.get("X-Demo-Mode", "normal")
        if mode == "reject":
            self._json(409, {"accepted": False, "reason": "external_policy_rejection"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        key = self.headers.get("Idempotency-Key", "")
        if not key:
            self._json(400, {"error": "missing_idempotency_key"})
            return
        try:
            record, created = self.store.apply(
                kind=kind,
                external_id=external_id,
                idempotency_key=key,
                payload=payload,
            )
        except ValueError as exc:
            self._json(409, {"accepted": False, "reason": str(exc)})
            return

        if mode == "accept_then_disconnect":
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.connection.close()
            return

        self._json(202, {"accepted": True, "created": created, "record": record})

    def do_GET(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] == "/stats":
            self._json(200, self.store.stats())
            return
        parts = self._parts()
        if parts is None:
            self._json(404, {"error": "not_found"})
            return
        kind, external_id = parts
        record = self.store.get(kind=kind, external_id=external_id)
        if record is None:
            self._json(404, {"applied": False})
            return
        self._json(200, {"applied": True, "record": record})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--ready", required=True)
    args = parser.parse_args()

    store = EffectStore(Path(args.db))
    server = ThreadingHTTPServer(("127.0.0.1", 0), EffectHandler)
    server.store = store  # type: ignore[attr-defined]
    Path(args.ready).write_text(json.dumps({"port": server.server_port}), encoding="utf-8")
    try:
        server.serve_forever(poll_interval=0.05)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
