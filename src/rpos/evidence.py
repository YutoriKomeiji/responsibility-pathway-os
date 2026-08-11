# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class EvaluationEvidenceClass(StrEnum):
    SAFETY_EVALUATION = "safety_evaluation"
    CAPABILITY_EVALUATION = "capability_evaluation"


_IMPORT_REQUIRED_FIELDS = {
    "evidence_id",
    "evidence_class",
    "source_system",
    "source_reference",
    "source_revision",
    "evaluation_scope",
    "result_summary",
}
_IMPORT_OPTIONAL_FIELDS = {"artifact_digest"}
_IMPORT_ALLOWED_FIELDS = _IMPORT_REQUIRED_FIELDS | _IMPORT_OPTIONAL_FIELDS


@dataclass(frozen=True)
class ExternalEvaluationEvidence:
    """Bounded evidence imported from an external evaluation system.

    Evaluation evidence can inform responsible review, but it is not an
    authorization decision, execution receipt, or operational effect readback.
    """

    evidence_id: str
    evidence_class: EvaluationEvidenceClass
    source_system: str
    source_reference: str
    evaluation_scope: str
    result_summary: str
    source_revision: str | None = None
    artifact_digest: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "source_system",
            "source_reference",
            "evaluation_scope",
            "result_summary",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if self.source_revision is not None and not self.source_revision.strip():
            raise ValueError("source_revision must not be empty when supplied")
        if self.artifact_digest is not None and not self.artifact_digest.strip():
            raise ValueError("artifact_digest must not be empty when supplied")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_import_dict(cls, value: dict[str, Any]) -> "ExternalEvaluationEvidence":
        fields = set(value)
        missing = sorted(_IMPORT_REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - _IMPORT_ALLOWED_FIELDS)
        if missing:
            raise ValueError(f"evaluation evidence is missing required fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"evaluation evidence contains unexpected fields: {', '.join(unexpected)}")

        artifact_digest = value.get("artifact_digest")
        return cls(
            evidence_id=str(value["evidence_id"]),
            evidence_class=EvaluationEvidenceClass(str(value["evidence_class"])),
            source_system=str(value["source_system"]),
            source_reference=str(value["source_reference"]),
            source_revision=str(value["source_revision"]),
            evaluation_scope=str(value["evaluation_scope"]),
            result_summary=str(value["result_summary"]),
            artifact_digest=None if artifact_digest is None else str(artifact_digest),
        )
