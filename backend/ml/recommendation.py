"""Business recommendations."""

from __future__ import annotations
from typing import Dict, List
from config import BUSINESS_CATALOG


def _best_sub_business(category, budget):
    subs = BUSINESS_CATALOG[category]["sub_businesses"]
    affordable = [s for s in subs if s["startup_cost"] <= budget]
    if affordable: return max(affordable, key=lambda s: s["startup_cost"])
    return min(subs, key=lambda s: s["startup_cost"])


def build_recommendations(opportunity_scores, features, budget, signals):
    recs = []
    ranked = sorted(opportunity_scores.items(), key=lambda x: -x[1])
    for category, score in ranked:
        cat_meta = BUSINESS_CATALOG[category]
        sub = _best_sub_business(category, budget)
        required = sub["startup_cost"]
        funding_gap = max(required - budget, 0.0)
        budget_fit = "Fits budget" if required <= budget else "Exceeds budget"
        reasons = _reasons_for(category, features)
        related_signals = [s["signal"] for s in signals if s.get("related_business_category") == category]
        recs.append({
            "business_category": category, "sub_business": sub["name"],
            "opportunity_score": round(float(score), 4),
            "estimated_investment": required, "budget_fit": budget_fit,
            "funding_gap": round(funding_gap, 2),
            "why_recommended": reasons, "related_opportunity_signals": related_signals,
            "cost_note": cat_meta["note"],
        })
    return recs


def _reasons_for(category, f):
    r = []
    if category == "Dairy / Milk-related Business":
        if f["veterinary"] > 0.4: r.append("Veterinary support present in the village.")
        if f["agri_activity"] > 0.3: r.append("Agriculture activity indicators relatively strong.")
        if f["transport"] > 0.4: r.append("Transport connectivity indicators present.")
        if f["dairy_district"] > 0.2: r.append("District dairy cooperative context is notable.")
    elif category == "Agri Processing":
        if f["cultivators"] > 0.25: r.append("Cultivator population relatively notable.")
        if f["agri_labour"] > 0.25: r.append("Agricultural labour presence relatively notable.")
        if f["crop_production"] > 0.15: r.append("District crop production context available.")
        if f["cultivated_area"] > 0.15: r.append("District cultivated area context available.")
        if f["irrigation"] > 0.1: r.append("District irrigation share is notable.")
        if f["market"] > 0.4: r.append("Market access indicator present.")
    elif category == "Retail & Trading":
        if f["population"] > 0.25: r.append("Village population base notable.")
        if f["market"] > 0.4: r.append("Mandi / market access present.")
        if f["banks"] > 0.4: r.append("Banking infrastructure present.")
        if f["transport"] > 0.4: r.append("Bus/transport connectivity present.")
        if f["workers"] > 0.2: r.append("Worker population notable.")
    elif category == "Skill & Repair Services":
        if f["govt_iti"] > 0.4: r.append("Government ITI / vocational presence.")
        if f["private_iti"] > 0.4: r.append("Private ITI / vocational presence.")
        if f["workers"] > 0.2: r.append("Worker population notable.")
        if f["population"] > 0.25: r.append("Population base supports service demand.")
        if f["transport"] > 0.4: r.append("Transport connectivity present.")
    elif category == "Rural Services":
        if f["population"] > 0.25: r.append("Population base supports rural services.")
        if f["banks"] > 0.4: r.append("Banking presence noted.")
        if f["transport"] > 0.4: r.append("Transport connectivity present.")
        if f["market"] > 0.4: r.append("Market presence noted.")
        if f["schools"] > 0.3: r.append("School presence noted.")
        if f["healthcare"] > 0.3: r.append("Health facility presence noted.")
    if not r: r.append("Signals are comparatively weaker for this category in the available data.")
    return r
