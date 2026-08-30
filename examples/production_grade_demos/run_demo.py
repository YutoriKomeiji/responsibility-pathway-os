# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from rpos import AdapterResult, OperationDefinition, ReceiptStatus, RposService
from rpos.models import ReconciliationResult, ReconciliationStatus


HERE = Path(__file__).resolve().parent


class HttpEffectAdapter:
    def __init__(self, base_url: str, *, kind: str, external_id: str, payload: dict[str, object], mode: str = "normal") -> None:
        self.url = f"{base_url}/effects/{kind}/{external_id}"
        self.payload = payload
        self.mode = mode

    def execute(self, *, operation_id: str, attempt_id: str, idempotency_key: str) -> AdapterResult:
        request = urllib.request.Request(
            self.url,
            data=json.dumps(self.payload, sort_keys=True).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Idempotency-Key": idempotency_key,
                "X-Demo-Mode": self.mode,
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=3) as response:
                receipt = json.loads(response.read())
        except urllib.error.HTTPError as exc:
            if exc.code == 409:
                return AdapterResult(
                    receipt_status=ReceiptStatus.FAILED,
                    receipt=json.loads(exc.read() or b"{}"),
                    readback_verified=False,
                    reason="external_service_rejected_request",
                )
            raise
        return AdapterResult(
            receipt_status=ReceiptStatus.SUCCEEDED,
            receipt=receipt,
            readback_verified=None,
            readback=None,
            reason="external_receipt_requires_independent_readback",
        )


class HttpReadbackObserver:
    def __init__(self, base_url: str, *, kind: str, external_id: str) -> None:
        self.url = f"{base_url}/effects/{kind}/{external_id}"

    def observe(self, *, operation_id: str, latest_attempt: dict[str, object] | None) -> ReconciliationResult:
        try:
            with urllib.request.urlopen(self.url, timeout=3) as response:
                payload = json.loads(response.read())
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return ReconciliationResult(
                    status=ReconciliationStatus.VERIFIED_NOT_APPLIED,
                    evidence={"url": self.url, "operation_id": operation_id},
                    reason="authoritative_http_readback_absent",
                )
            return ReconciliationResult(
                status=ReconciliationStatus.UNRESOLVED,
                evidence={"url": self.url, "http_status": exc.code},
                reason="authoritative_http_readback_unavailable",
            )
        record = payload.get("record", {})
        expected_key = str((latest_attempt or {}).get("idempotency_key") or "")
        if payload.get("applied") is True and record.get("idempotency_key") == expected_key:
            return ReconciliationResult(
                status=ReconciliationStatus.VERIFIED_APPLIED,
                evidence={"url": self.url, "record": record},
                reason="authoritative_http_readback_verified",
            )
        return ReconciliationResult(
            status=ReconciliationStatus.UNRESOLVED,
            evidence={"url": self.url, "payload": payload},
            reason="authoritative_http_readback_identity_mismatch",
        )


def definition(operation_id: str, action_name: str, *, approval_authority: str) -> OperationDefinition:
    return OperationDefinition(
        operation_id=operation_id,
        action_name=action_name,
        requested_by="automation_service",
        execution_actor="integration_worker",
        approval_authority=approval_authority,
        human_return_point=f"{approval_authority}-review",
        residual_owner="operations_team",
        resume_authority=approval_authority,
        requires_human_gate=True,
        verification_required=True,
    )


def payment_dispatch(workdir: Path, base_url: str) -> dict[str, object]:
    service = RposService(str(workdir / "payment-rpos.db"))
    operation_id = "supplier-payment-2026-001"
    service.propose(definition(operation_id, "release_supplier_payment", approval_authority="finance_approver"))
    service.approve(operation_id, actor="finance_approver")
    result = service.dispatch(
        operation_id,
        attempt_id="payment-attempt-1",
        idempotency_key="invoice-INV-2026-001",
        adapter=HttpEffectAdapter(
            base_url,
            kind="payment",
            external_id="INV-2026-001",
            payload={"supplier": "demo-supplier", "amount": 125000, "currency": "JPY"},
            mode="accept_then_disconnect",
        ),
    )
    return {"state": result.state.value, "events": service.event_history(operation_id)}


def payment_reconcile(workdir: Path, base_url: str) -> dict[str, object]:
    service = RposService(str(workdir / "payment-rpos.db"))
    operation_id = "supplier-payment-2026-001"
    before = service.inspect(operation_id)
    final = service.reconcile(
        operation_id,
        actor="operations_team",
        observer=HttpReadbackObserver(base_url, kind="payment", external_id="INV-2026-001"),
    )
    return {
        "state_before_restart_reconcile": before.state.value,
        "final_state": final.state.value,
        "events": service.event_history(operation_id),
    }


def deployment_repair(workdir: Path, base_url: str) -> dict[str, object]:
    service = RposService(str(workdir / "deployment-rpos.db"))
    operation_id = "production-deploy-2026-001"
    service.propose(definition(operation_id, "promote_production_release", approval_authority="change_manager"))
    service.approve(operation_id, actor="change_manager")
    rejected = service.dispatch(
        operation_id,
        attempt_id="deploy-attempt-1",
        idempotency_key="deploy-rejected-attempt-1",
        adapter=HttpEffectAdapter(
            base_url,
            kind="deployment",
            external_id="release-2026.08.30",
            payload={"service": "orders-api", "version": "2026.08.30", "environment": "production"},
            mode="reject",
        ),
    )
    service.prepare_repair(
        operation_id,
        actor="operations_team",
        summary="external deployment controller rejection reviewed; retry authorized after correction",
    )
    resumed = service.resume(operation_id, actor="change_manager")
    dispatched = service.dispatch(
        operation_id,
        attempt_id="deploy-attempt-2",
        idempotency_key="deploy-release-2026.08.30",
        adapter=HttpEffectAdapter(
            base_url,
            kind="deployment",
            external_id="release-2026.08.30",
            payload={"service": "orders-api", "version": "2026.08.30", "environment": "production"},
        ),
    )
    final = service.reconcile(
        operation_id,
        actor="operations_team",
        observer=HttpReadbackObserver(base_url, kind="deployment", external_id="release-2026.08.30"),
    )
    return {
        "first_state": rejected.state.value,
        "resumed_state": resumed.state.value,
        "dispatch_state": dispatched.state.value,
        "final_state": final.state.value,
        "events": service.event_history(operation_id),
    }


def access_denied(workdir: Path, base_url: str) -> dict[str, object]:
    service = RposService(str(workdir / "access-rpos.db"))
    operation_id = "privileged-access-revoke-2026-001"
    proposed = service.propose(definition(operation_id, "revoke_privileged_access", approval_authority="security_duty_manager"))
    denied = service.deny(
        operation_id,
        actor="security_duty_manager",
        reason="identity investigation incomplete; do not execute revocation yet",
    )
    return {
        "proposed_state": proposed.state.value,
        "final_state": denied.state.value,
        "external_url_not_called": f"{base_url}/effects/access/admin-demo",
        "events": service.event_history(operation_id),
    }


def _run_worker(name: str, workdir: Path, base_url: str) -> dict[str, object]:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        name,
        "--workdir",
        str(workdir),
        "--base-url",
        base_url,
    ]
    completed = subprocess.run(command, check=False, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(
            f"worker {name!r} failed with code {completed.returncode}; "
            f"stdout={completed.stdout!r}; stderr={completed.stderr!r}"
        )
    return json.loads(completed.stdout)


def _read_json(url: str) -> dict[str, object]:
    with urllib.request.urlopen(url, timeout=3) as response:
        return json.loads(response.read())


def run_suite(workdir: Path) -> dict[str, object]:
    ready = workdir / "external-ready.json"
    process = subprocess.Popen(
        [
            sys.executable,
            str(HERE / "external_service.py"),
            "--db",
            str(workdir / "external-effects.db"),
            "--ready",
            str(ready),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        deadline = time.monotonic() + 5
        while not ready.exists():
            if process.poll() is not None:
                stderr = process.stderr.read() if process.stderr else ""
                raise RuntimeError(f"external service exited early: {stderr}")
            if time.monotonic() > deadline:
                raise TimeoutError("external service did not become ready")
            time.sleep(0.05)
        base_url = f"http://127.0.0.1:{json.loads(ready.read_text(encoding='utf-8'))['port']}"

        payment_first = _run_worker("payment-dispatch", workdir, base_url)
        payment_after_restart = _run_worker("payment-reconcile", workdir, base_url)
        deployment = _run_worker("deployment-repair", workdir, base_url)
        access = _run_worker("access-denied", workdir, base_url)
        stats = _read_json(f"{base_url}/stats")

        effects = {(item["kind"], item["external_id"]): item for item in stats["effects"]}
        payment_effect = effects[("payment", "INV-2026-001")]
        deployment_effect = effects[("deployment", "release-2026.08.30")]
        access_effects = [item for item in stats["effects"] if item["kind"] == "access"]

        result = {
            "supplier_payment": {
                "dispatch": payment_first,
                "after_real_process_restart": payment_after_restart,
                "external_apply_count": payment_effect["apply_count"],
            },
            "production_deployment": {
                "pathway": deployment,
                "external_apply_count": deployment_effect["apply_count"],
            },
            "privileged_access_revocation": {
                "pathway": access,
                "external_apply_count": len(access_effects),
            },
            "external_effect_count": stats["effect_count"],
        }
        if payment_first["state"] != "effect_unknown":
            raise AssertionError("payment ambiguity was not preserved")
        if payment_after_restart["state_before_restart_reconcile"] != "effect_unknown":
            raise AssertionError("payment unresolved state did not survive process restart")
        if payment_after_restart["final_state"] != "completed" or payment_effect["apply_count"] != 1:
            raise AssertionError("payment was not reconciled exactly once")
        if deployment["first_state"] != "repair_required" or deployment["final_state"] != "completed":
            raise AssertionError("deployment repair/resume path failed")
        if deployment_effect["apply_count"] != 1:
            raise AssertionError("deployment external effect count mismatch")
        if access["final_state"] != "denied" or access_effects:
            raise AssertionError("denied access operation produced an external effect")
        return result
    finally:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", choices=["payment-dispatch", "payment-reconcile", "deployment-repair", "access-denied"])
    parser.add_argument("--workdir")
    parser.add_argument("--base-url")
    args = parser.parse_args()

    if args.worker:
        if not args.workdir or not args.base_url:
            parser.error("--worker requires --workdir and --base-url")
        workers = {
            "payment-dispatch": payment_dispatch,
            "payment-reconcile": payment_reconcile,
            "deployment-repair": deployment_repair,
            "access-denied": access_denied,
        }
        print(json.dumps(workers[args.worker](Path(args.workdir), args.base_url), sort_keys=True))
        return 0

    if args.workdir:
        workdir = Path(args.workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        print(json.dumps(run_suite(workdir), indent=2, sort_keys=True))
        return 0

    with tempfile.TemporaryDirectory(prefix="rpos-operational-demo-") as temp_dir:
        print(json.dumps(run_suite(Path(temp_dir)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
