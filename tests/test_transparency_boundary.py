# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

import pytest

from rpos.transparency import (
    AIInteractionDisclosure,
    HumanEditorialResponsibility,
    SyntheticContentProvenance,
    TransparencyDutyClass,
    TransparencyEnvelope,
    TransparencyStatus,
    disclosure_grants_authority,
    human_review_proves_legal_compliance,
    marker_proves_content_truth,
)


def _envelope(duty: TransparencyDutyClass, status: TransparencyStatus = TransparencyStatus.REQUIRED_PENDING) -> TransparencyEnvelope:
    return TransparencyEnvelope(
        operation_id="op-transparency-1",
        provider_or_deployer_role="provider",
        transparency_duty_class=duty,
        content_or_interaction_id="subject-1",
        responsible_actor="operator-1",
        status=status,
    )


def test_ai_interaction_disclosure_does_not_grant_authority() -> None:
    record = AIInteractionDisclosure(
        envelope=_envelope(TransparencyDutyClass.AI_INTERACTION),
        disclosure_text="You are interacting with an AI system.",
        disclosure_surface="first-run-dialog",
        presented=True,
        presentation_evidence_ref="evidence://interaction-disclosure/1",
    )
    assert disclosure_grants_authority(record) is False


def test_synthetic_marker_does_not_prove_content_truth() -> None:
    record = SyntheticContentProvenance(
        envelope=_envelope(TransparencyDutyClass.SYNTHETIC_CONTENT, TransparencyStatus.VERIFIED),
        content_hash="sha256:example",
        generation_class="ai_generated_text",
        marker_profile="rpos.synthetic-marker.v0.1",
        marker_inserted=True,
        marker_verified=True,
        marker_evidence_ref="evidence://marker/1",
    )
    assert marker_proves_content_truth(record) is False


def test_marker_receipt_cannot_claim_verification_without_inserted_marker() -> None:
    with pytest.raises(ValueError, match="marker cannot be verified"):
        SyntheticContentProvenance(
            envelope=_envelope(TransparencyDutyClass.SYNTHETIC_CONTENT),
            content_hash="sha256:example",
            generation_class="ai_generated_text",
            marker_profile="rpos.synthetic-marker.v0.1",
            marker_inserted=False,
            marker_verified=True,
        )


def test_human_review_does_not_prove_legal_compliance() -> None:
    record = HumanEditorialResponsibility(
        envelope=_envelope(TransparencyDutyClass.HUMAN_EDITORIAL_REVIEW),
        reviewed=True,
        reviewer="editor-1",
        editorial_control_summary="Reviewed before publication.",
    )
    assert human_review_proves_legal_compliance(record) is False


def test_verified_status_is_explicit_not_inferred_from_evidence_ref() -> None:
    envelope = TransparencyEnvelope(
        operation_id="op-transparency-2",
        provider_or_deployer_role="deployer",
        transparency_duty_class=TransparencyDutyClass.DEPLOYER_DISCLOSURE,
        content_or_interaction_id="content-2",
        responsible_actor="publisher-1",
        status=TransparencyStatus.PRESENTED_UNVERIFIED,
        evidence_refs=("evidence://rendered-disclosure/2",),
    )
    assert envelope.status is TransparencyStatus.PRESENTED_UNVERIFIED


def test_wrong_record_duty_class_is_rejected() -> None:
    with pytest.raises(ValueError, match="ai_interaction"):
        AIInteractionDisclosure(
            envelope=_envelope(TransparencyDutyClass.SYNTHETIC_CONTENT),
            disclosure_text="AI disclosure",
            disclosure_surface="dialog",
        )
