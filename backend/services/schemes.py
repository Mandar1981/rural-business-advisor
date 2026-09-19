"""PMEGP relevance section."""

from __future__ import annotations
from config import PMEGP


def pmegp_relevance(budget, funding_gap):
    return {"scheme_name": PMEGP["scheme_name"], "potential_relevance": PMEGP["potential_relevance_note"],
            "checklist": PMEGP["checklist"], "user_budget": round(budget, 2),
            "estimated_funding_gap": round(funding_gap, 2),
            "verification_warning": PMEGP["verification_warning"]}
