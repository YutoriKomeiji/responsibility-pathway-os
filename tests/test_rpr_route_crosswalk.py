# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
import pytest

from rpos.rpr_route_crosswalk import (
    CrosswalkDisposition,
    RPR_ROUTE_CLASSES,
    crosswalk_rpr_route_class,
)
from rpos.routing import ResponsibilityRouteKind


def test_reconciliation_route_has_only_semantic_equivalence():
    disposition, kind = crosswalk_rpr_route_class("hold_for_reconciliation")
    assert disposition is CrosswalkDisposition.SEMANTIC_MATCH_ONLY
    assert kind is ResponsibilityRouteKind.HOLD_FOR_RECONCILIATION


@pytest.mark.parametrize("name", sorted(RPR_ROUTE_CLASSES - {"hold_for_reconciliation"}))
def test_other_rpr_routes_require_contextual_review_not_automatic_authority(name):
    disposition, kind = crosswalk_rpr_route_class(name)
    assert disposition is CrosswalkDisposition.REQUIRES_CONTEXTUAL_REVIEW
    assert kind is None


def test_human_return_is_not_implicitly_rpos_human_gate():
    disposition, kind = crosswalk_rpr_route_class("bounded_human_return")
    assert kind is None
    assert disposition is CrosswalkDisposition.REQUIRES_CONTEXTUAL_REVIEW


def test_unknown_route_fails_explicitly():
    with pytest.raises(ValueError, match="unknown RPR"):
        crosswalk_rpr_route_class("human_gate")
