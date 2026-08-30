# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "production_grade_demos" / "run_demo.py"


def test_production_grade_operational_demo_suite() -> None:
    completed = subprocess.run(
        [sys.executable, str(DEMO)],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert completed.returncode == 0, (
        f"operational demo failed with code {completed.returncode}\n"
        f"stdout:\n{completed.stdout}\n"
        f"stderr:\n{completed.stderr}"
    )
    result = json.loads(completed.stdout)

    payment = result["supplier_payment"]
    assert payment["dispatch"]["state"] == "effect_unknown"
    assert payment["after_real_process_restart"]["state_before_restart_reconcile"] == "effect_unknown"
    assert payment["after_real_process_restart"]["final_state"] == "completed"
    assert payment["external_apply_count"] == 1

    deployment = result["production_deployment"]
    assert deployment["pathway"]["first_state"] == "repair_required"
    assert deployment["pathway"]["dispatch_state"] == "effect_unknown"
    assert deployment["pathway"]["final_state"] == "completed"
    assert deployment["external_apply_count"] == 1

    access = result["privileged_access_revocation"]
    assert access["pathway"]["proposed_state"] == "human_gate"
    assert access["pathway"]["final_state"] == "denied"
    assert access["external_apply_count"] == 0

    assert result["external_effect_count"] == 2
