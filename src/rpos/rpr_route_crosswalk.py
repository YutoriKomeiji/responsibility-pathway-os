# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
"""A bounded, dependency-free semantic crosswalk, not automatic route transfer.

RPR has different route vocabulary and a richer envelope; RPOS operations
cannot adopt an RPR route just by matching a string.
"""
from __future__ import annotations

from enum import StrEnum

from .routing import ResponsibilityRouteKind


class CrosswalkDisposition(StrEnum):
    SEMANTIC_MATCH_ONLY = "semantic_match_only"
    REQUIRES_CONTEXTUAL_REVIEW = "requires_contextual_review"


# Source vocabulary verified against RPR src/rpr/models.py on 2026-10-25.
RPR_ROUTE_CLASSES = frozenset({
    "continue_autonomously",
    "ai_resolve_within_delegation",
    "hold_for_reconciliation",
    "bounded_human_return",
    "stop_and_preserve_residue",
})


def crosswalk_rpr_route_class(value: str) -> tuple[CrosswalkDisposition, ResponsibilityRouteKind | None]:
    """Return semantic equivalence only; never grant execution/receiver authority.

    A human-return declaration cannot be blindly mapped to RPOS HUMAN_GATE;
    it requires the operation's actual approval state and eligible receiver.
    Other RPR route classes have no safe one-to-one RPOS operation-state class.
    """
    if value not in RPR_ROUTE_CLASSES:
        raise ValueError("unknown RPR responsibility route class")
    if value == "hold_for_reconciliation":
        return CrosswalkDisposition.SEMANTIC_MATCH_ONLY, ResponsibilityRouteKind.HOLD_FOR_RECONCILIATION
    return CrosswalkDisposition.REQUIRES_CONTEXTUAL_REVIEW, None
