# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from rpos.security import SecurityDisposition
from rpos.security_policy import (
    EvidenceSupersessionRecord,
    ResponsibilityDependencyCriticality,
    ResponsibilityDependencyHealth,
    ResponsibilityDependencyStatus,
    evaluate_responsibility_degradation,
    validate_evidence_supersession_chain,
)


def test_evidence_supersession_chain_preserves_explicit_lineage() -> None:
    result = validate_evidence_supersession_chain(
        [
            EvidenceSupersessionRecord("ev-1", "sha256:a", "eval://1"),
            EvidenceSupersessionRecord("ev-2", "sha256:b", "eval://2", supersedes_id="ev-1", reason="newer run"),
            EvidenceSupersessionRecord("ev-3", "sha256:c", "eval://3", supersedes_id="ev-2", reason="corrected scope"),
        ]
    )
    assert result.valid is True
    assert result.reasons == ()
    assert result.head_evidence_id == "ev-3"


def test_evidence_supersession_rejects_silent_replacement() -> None:
    result = validate_evidence_supersession_chain(
        [
            EvidenceSupersessionRecord("ev-1", "sha256:a", "eval://1"),
            EvidenceSupersessionRecord("ev-2", "sha256:b", "eval://2"),
        ]
    )
    assert result.valid is False
    assert "silent_replacement_without_supersession:ev-2" in result.reasons


def test_evidence_supersession_rejects_broken_predecessor() -> None:
    result = validate_evidence_supersession_chain(
        [
            EvidenceSupersessionRecord("ev-1", "sha256:a", "eval://1"),
            EvidenceSupersessionRecord("ev-2", "sha256:b", "eval://2", supersedes_id="unknown"),
        ]
    )
    assert result.valid is False
    assert any(reason.startswith("broken_supersession_link:ev-2") for reason in result.reasons)


def test_evidence_supersession_rejects_duplicate_identity() -> None:
    result = validate_evidence_supersession_chain(
        [
            EvidenceSupersessionRecord("ev-1", "sha256:a", "eval://1"),
            EvidenceSupersessionRecord("ev-2", "sha256:b", "eval://2", supersedes_id="ev-1"),
            EvidenceSupersessionRecord("ev-1", "sha256:c", "eval://3", supersedes_id="ev-2"),
        ]
    )
    assert result.valid is False
    assert "duplicate_evidence_id:ev-1" in result.reasons


def test_evidence_record_rejects_self_supersession_at_construction() -> None:
    try:
        EvidenceSupersessionRecord("ev-1", "sha256:a", "eval://1", supersedes_id="ev-1")
    except ValueError as exc:
        assert "cannot supersede itself" in str(exc)
    else:
        raise AssertionError("self-supersession must be rejected")


def test_degradation_fails_closed_when_authority_dependency_is_degraded() -> None:
    decision = evaluate_responsibility_degradation(
        [
            ResponsibilityDependencyStatus(
                "authority-service",
                ResponsibilityDependencyCriticality.AUTHORITY,
                ResponsibilityDependencyHealth.DEGRADED,
            )
        ]
    )
    assert decision.disposition is SecurityDisposition.HOLD
    assert decision.allowed is False
    assert "authority-service" in decision.degraded_dependencies


def test_degradation_fails_closed_when_effect_verification_is_unavailable() -> None:
    decision = evaluate_responsibility_degradation(
        [
            ResponsibilityDependencyStatus(
                "effect-readback",
                ResponsibilityDependencyCriticality.EFFECT_VERIFICATION,
                ResponsibilityDependencyHealth.UNAVAILABLE,
            )
        ]
    )
    assert decision.disposition is SecurityDisposition.HOLD
    assert any("effect_verification" in reason for reason in decision.reasons)


def test_supporting_dependency_may_degrade_but_remains_observable() -> None:
    decision = evaluate_responsibility_degradation(
        [
            ResponsibilityDependencyStatus(
                "optional-metrics",
                ResponsibilityDependencyCriticality.SUPPORTING,
                ResponsibilityDependencyHealth.UNAVAILABLE,
            )
        ]
    )
    assert decision.disposition is SecurityDisposition.ALLOW
    assert decision.allowed is True
    assert decision.degraded_dependencies == ("optional-metrics",)
    assert decision.reasons == ("supporting_dependency_unavailable:optional-metrics",)


def test_mixed_degradation_never_lets_supporting_availability_override_critical_failure() -> None:
    decision = evaluate_responsibility_degradation(
        [
            ResponsibilityDependencyStatus(
                "metrics",
                ResponsibilityDependencyCriticality.SUPPORTING,
                ResponsibilityDependencyHealth.AVAILABLE,
            ),
            ResponsibilityDependencyStatus(
                "identity-provider",
                ResponsibilityDependencyCriticality.IDENTITY,
                ResponsibilityDependencyHealth.UNAVAILABLE,
            ),
        ]
    )
    assert decision.disposition is SecurityDisposition.HOLD
