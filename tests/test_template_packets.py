# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
from pathlib import Path

import pytest

from rpos.template_packets import (
    PacketTemplateKind,
    ResponsibilityPacket,
    ResponsibilityStateEnvelope,
    validate_envelope,
    validate_packet,
)


RPOS_ROOT = Path(__file__).resolve().parents[1]
CATALOG = RPOS_ROOT / "templates" / "catalog.json"


def _catalog_templates() -> list[dict[str, object]]:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    assert data["schema_version"] == "rpos.packet-template-catalog.v0.1"
    assert data["authority_effect"] == "none"
    return data["templates"]


def test_catalog_contains_every_supported_template_kind() -> None:
    envelopes = _catalog_templates()
    kinds = {validate_envelope(envelope).template_kind for envelope in envelopes}
    assert kinds == set(PacketTemplateKind)


def test_catalog_templates_are_state_and_authority_neutral() -> None:
    for raw in _catalog_templates():
        envelope = validate_envelope(raw)
        assert envelope.authority_effect == "none"
        assert envelope.to_dict()["authority_effect"] == "none"


def test_legacy_packet_api_remains_compatible() -> None:
    raw = _catalog_templates()[0]
    current = validate_envelope(raw)
    legacy = validate_packet(raw)
    assert isinstance(current, ResponsibilityStateEnvelope)
    assert isinstance(legacy, ResponsibilityPacket)
    assert current.to_dict() == legacy.to_dict()


def test_new_envelope_schema_identifier_is_supported() -> None:
    raw = json.loads(json.dumps(_catalog_templates()[0]))
    raw["schema_version"] = "rpos.responsibility-state-envelope.v0.1"
    envelope = validate_envelope(raw)
    assert envelope.schema_version == "rpos.responsibility-state-envelope.v0.1"


def test_unknown_envelope_field_fails_closed() -> None:
    raw = dict(_catalog_templates()[0])
    raw["legal_conclusion"] = "allowed"
    with pytest.raises(ValueError, match="unknown envelope fields"):
        validate_envelope(raw)


def test_unknown_payload_field_fails_closed() -> None:
    raw = json.loads(json.dumps(_catalog_templates()[0]))
    raw["payload"]["implicit_authorization"] = True
    with pytest.raises(ValueError, match="unknown payload fields"):
        validate_envelope(raw)


def test_missing_required_payload_field_fails_closed() -> None:
    raw = json.loads(json.dumps(_catalog_templates()[0]))
    del raw["payload"]["approval_authority"]
    with pytest.raises(ValueError, match="missing payload fields"):
        validate_envelope(raw)


def test_template_cannot_claim_authority_effect() -> None:
    raw = json.loads(json.dumps(_catalog_templates()[1]))
    raw["authority_effect"] = "authorized"
    with pytest.raises(ValueError, match="cannot create authority"):
        validate_envelope(raw)
