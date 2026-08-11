# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
from pathlib import Path

import pytest

from rpos.template_packets import PacketTemplateKind, validate_packet


RPOS_ROOT = Path(__file__).resolve().parents[1]
CATALOG = RPOS_ROOT / "templates" / "catalog.json"


def _catalog_templates() -> list[dict[str, object]]:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    assert data["schema_version"] == "rpos.packet-template-catalog.v0.1"
    assert data["authority_effect"] == "none"
    return data["templates"]


def test_catalog_contains_every_supported_template_kind() -> None:
    packets = _catalog_templates()
    kinds = {validate_packet(packet).template_kind for packet in packets}
    assert kinds == set(PacketTemplateKind)


def test_catalog_templates_are_state_and_authority_neutral() -> None:
    for raw in _catalog_templates():
        packet = validate_packet(raw)
        assert packet.authority_effect == "none"
        assert packet.to_dict()["authority_effect"] == "none"


def test_unknown_envelope_field_fails_closed() -> None:
    raw = dict(_catalog_templates()[0])
    raw["legal_conclusion"] = "allowed"
    with pytest.raises(ValueError, match="unknown packet fields"):
        validate_packet(raw)


def test_unknown_payload_field_fails_closed() -> None:
    raw = json.loads(json.dumps(_catalog_templates()[0]))
    raw["payload"]["implicit_authorization"] = True
    with pytest.raises(ValueError, match="unknown payload fields"):
        validate_packet(raw)


def test_missing_required_payload_field_fails_closed() -> None:
    raw = json.loads(json.dumps(_catalog_templates()[0]))
    del raw["payload"]["approval_authority"]
    with pytest.raises(ValueError, match="missing payload fields"):
        validate_packet(raw)


def test_template_cannot_claim_authority_effect() -> None:
    raw = json.loads(json.dumps(_catalog_templates()[1]))
    raw["authority_effect"] = "authorized"
    with pytest.raises(ValueError, match="cannot create authority"):
        validate_packet(raw)
