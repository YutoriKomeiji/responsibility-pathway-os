# Copyright (c) 2026 RPOS contributors
# SPDX-License-Identifier: MIT
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class DependencyEvidenceClass(StrEnum):
    SOFTWARE_COMPONENT = "software_component"
    ADAPTER = "adapter"
    EXTERNAL_SERVICE = "external_service"


_IMPORT_REQUIRED_FIELDS = {
    "evidence_id",
    "evidence_class",
    "source_system",
    "source_reference",
    "source_revision",
    "component_name",
    "component_version",
    "dependency_owner",
    "verification_method",
}
_IMPORT_OPTIONAL_FIELDS = {
    "artifact_digest",
    "supplier_role",
    "unresolved_risk",
}
_IMPORT_ALLOWED_FIELDS = _IMPORT_REQUIRED_FIELDS | _IMPORT_OPTIONAL_FIELDS


@dataclass(frozen=True)
class DependencyEvidence:
    """Bounded software supply-chain evidence attached to a responsibility pathway.

    Dependency evidence records provenance and responsibility facts. It does not
    authorize execution, verify an external effect, establish supplier trust, or
    prove conformance with any cybersecurity guideline.
    """

    evidence_id: str
    evidence_class: DependencyEvidenceClass
    source_system: str
    source_reference: str
    source_revision: str
    component_name: str
    component_version: str
    dependency_owner: str
    verification_method: str
    artifact_digest: str | None = None
    supplier_role: str | None = None
    unresolved_risk: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "source_system",
            "source_reference",
            "source_revision",
            "component_name",
            "component_version",
            "dependency_owner",
            "verification_method",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        for name in ("artifact_digest", "supplier_role", "unresolved_risk"):
            value = getattr(self, name)
            if value is not None and not value.strip():
                raise ValueError(f"{name} must not be empty when supplied")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_import_dict(cls, value: dict[str, Any]) -> "DependencyEvidence":
        fields = set(value)
        missing = sorted(_IMPORT_REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - _IMPORT_ALLOWED_FIELDS)
        if missing:
            raise ValueError(f"dependency evidence is missing required fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"dependency evidence contains unexpected fields: {', '.join(unexpected)}")

        def optional(name: str) -> str | None:
            item = value.get(name)
            return None if item is None else str(item)

        return cls(
            evidence_id=str(value["evidence_id"]),
            evidence_class=DependencyEvidenceClass(str(value["evidence_class"])),
            source_system=str(value["source_system"]),
            source_reference=str(value["source_reference"]),
            source_revision=str(value["source_revision"]),
            component_name=str(value["component_name"]),
            component_version=str(value["component_version"]),
            dependency_owner=str(value["dependency_owner"]),
            verification_method=str(value["verification_method"]),
            artifact_digest=optional("artifact_digest"),
            supplier_role=optional("supplier_role"),
            unresolved_risk=optional("unresolved_risk"),
        )
