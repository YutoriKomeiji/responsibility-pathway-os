# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .audit import AuditEvidenceSource, build_audit_evidence_package


@dataclass(frozen=True)
class GuidelineEvidenceMapping:
    mapping_id: str
    expectation: str
    evidence_groups: tuple[str, ...]
    mechanism_summary: str
    not_proven: tuple[str, ...]


JAPAN_AI_GUIDELINES_V1_2_PARTIAL: tuple[GuidelineEvidenceMapping, ...] = (
    GuidelineEvidenceMapping(
        mapping_id="jp-aigb-v1.2-info-001",
        expectation="retain bounded information about evaluated capability, limitations, safety or social-risk evidence for responsible review",
        evidence_groups=("evaluation",),
        mechanism_summary="external evaluation evidence records preserve declared scope, source reference, source revision, result summary, and optional artifact digest",
        not_proven=("official_certification", "general_ai_safety", "legal_or_regulatory_compliance"),
    ),
    GuidelineEvidenceMapping(
        mapping_id="jp-aigb-v1.2-human-001",
        expectation="make human authority and accountability boundaries inspectable for consequential operations",
        evidence_groups=("authority_and_admission",),
        mechanism_summary="Human Gate, declared authority, residual owner, and Human Return evidence remain distinct from capability and execution",
        not_proven=("organizational_governance_sufficiency", "legal_responsibility", "legal_or_regulatory_compliance"),
    ),
    GuidelineEvidenceMapping(
        mapping_id="jp-aigb-v1.2-monitor-001",
        expectation="retain monitoring, external-effect observation, and recovery evidence without converting ambiguity into success",
        evidence_groups=("execution_and_receipt", "external_effect_readback", "recovery_and_resume"),
        mechanism_summary="receipt, independent readback, unresolved state, repair, resume, and residual responsibility are exported as separate evidence classes",
        not_proven=("external_system_correctness", "incident_response_sufficiency", "legal_or_regulatory_compliance"),
    ),
)


def build_guideline_evidence_matrix(
    source: AuditEvidenceSource,
    operation_id: str,
    *,
    mappings: Iterable[GuidelineEvidenceMapping] = JAPAN_AI_GUIDELINES_V1_2_PARTIAL,
) -> dict[str, Any]:
    audit = build_audit_evidence_package(source, operation_id)
    evidence = audit["evidence"]
    rows: list[dict[str, Any]] = []

    for mapping in mappings:
        group_counts = {group: len(evidence.get(group, [])) for group in mapping.evidence_groups}
        missing_groups = [group for group, count in group_counts.items() if count == 0]
        rows.append(
            {
                "mapping_id": mapping.mapping_id,
                "expectation": mapping.expectation,
                "mechanism_summary": mapping.mechanism_summary,
                "evidence_group_counts": group_counts,
                "evidence_status": "gap" if missing_groups else "evidence_present",
                "missing_evidence_groups": missing_groups,
                "not_proven": list(mapping.not_proven),
            }
        )

    return {
        "schema_version": "rpos.guideline-matrix.v0.1",
        "profile": "jp-ai-guidelines-for-business-v1.2-partial-engineering-map",
        "profile_scope": "partial engineering evidence mapping; not a compliance checklist or official endorsement",
        "operation_id": operation_id,
        "current_state": audit["current_state"],
        "rows": rows,
        "global_not_proven": audit["not_proven"],
    }
