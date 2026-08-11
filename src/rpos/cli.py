# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Sequence

from .audit import build_audit_evidence_package
from .dependency import DependencyEvidence
from .evidence import ExternalEvaluationEvidence
from .guideline import build_guideline_evidence_matrix
from .models import OperationDefinition
from .service import RposService


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _emit(value: Any, *, stream: Any | None = None) -> None:
    target = sys.stdout if stream is None else stream
    print(json.dumps(_jsonable(value), ensure_ascii=False, sort_keys=True), file=target)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rpos")
    parser.add_argument("--db", default="rpos.db", help="SQLite database path")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("boot")
    sub.add_parser("unresolved")

    inspect = sub.add_parser("inspect")
    inspect.add_argument("operation_id")

    events = sub.add_parser("events")
    events.add_argument("operation_id")

    audit = sub.add_parser("audit")
    audit.add_argument("operation_id")

    guideline = sub.add_parser("guideline-matrix")
    guideline.add_argument("operation_id")

    evaluation = sub.add_parser("record-evaluation-json")
    evaluation.add_argument("operation_id")
    evaluation.add_argument("path")
    evaluation.add_argument("--actor", required=True)

    dependency = sub.add_parser("record-dependency-json")
    dependency.add_argument("operation_id")
    dependency.add_argument("path")
    dependency.add_argument("--actor", required=True)

    propose = sub.add_parser("propose-json")
    propose.add_argument("path")

    approve = sub.add_parser("approve")
    approve.add_argument("operation_id")
    approve.add_argument("--actor", required=True)

    deny = sub.add_parser("deny")
    deny.add_argument("operation_id")
    deny.add_argument("--actor", required=True)
    deny.add_argument("--reason", required=True)

    repair = sub.add_parser("prepare-repair")
    repair.add_argument("operation_id")
    repair.add_argument("--actor", required=True)
    repair.add_argument("--summary", required=True)

    resume = sub.add_parser("resume")
    resume.add_argument("operation_id")
    resume.add_argument("--actor", required=True)
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    service = RposService(args.db)
    try:
        if args.command == "boot":
            result = service.boot_report()
        elif args.command == "unresolved":
            result = {"operation_ids": service.list_unresolved()}
        elif args.command == "inspect":
            result = service.inspect(args.operation_id)
        elif args.command == "events":
            result = {"operation_id": args.operation_id, "events": service.event_history(args.operation_id)}
        elif args.command == "audit":
            result = build_audit_evidence_package(service, args.operation_id)
        elif args.command == "guideline-matrix":
            result = build_guideline_evidence_matrix(service, args.operation_id)
        elif args.command == "record-evaluation-json":
            payload = json.loads(Path(args.path).read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("evaluation evidence JSON must contain an object")
            evidence = ExternalEvaluationEvidence.from_import_dict(payload)
            result = service.record_evaluation_evidence(args.operation_id, actor=args.actor, evidence=evidence)
        elif args.command == "record-dependency-json":
            payload = json.loads(Path(args.path).read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("dependency evidence JSON must contain an object")
            evidence = DependencyEvidence.from_import_dict(payload)
            result = service.record_dependency_evidence(args.operation_id, actor=args.actor, evidence=evidence)
        elif args.command == "propose-json":
            payload = json.loads(Path(args.path).read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("proposal JSON must contain an object")
            result = service.propose(OperationDefinition.from_dict(payload))
        elif args.command == "approve":
            result = service.approve(args.operation_id, actor=args.actor)
        elif args.command == "deny":
            result = service.deny(args.operation_id, actor=args.actor, reason=args.reason)
        elif args.command == "prepare-repair":
            result = service.prepare_repair(args.operation_id, actor=args.actor, summary=args.summary)
        elif args.command == "resume":
            result = service.resume(args.operation_id, actor=args.actor)
        else:
            raise ValueError(f"unsupported command: {args.command}")
    except (OSError, json.JSONDecodeError, KeyError, ValueError, PermissionError) as exc:
        _emit({"error": type(exc).__name__, "message": str(exc)}, stream=sys.stderr)
        return 2

    _emit(result)
    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()