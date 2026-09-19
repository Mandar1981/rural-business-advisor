"""Opportunity Signal / Gap Engine."""

from __future__ import annotations
from typing import Dict, List
import numpy as np
import pandas as pd
from config import AMENITY_FEATURES


def _num(v, default=0.0):
    try:
        if v is None or (isinstance(v, float) and np.isnan(v)): return default
        return float(v)
    except Exception: return default


def _safe_norm(value, cap):
    if cap <= 0: return 0.0
    return float(min(max(value, 0.0) / cap, 1.0))


def compute_raw_features(village_row, district_ctx):
    f = {}
    pop = _num(village_row.get("Total Population Person"))
    workers = _num(village_row.get("Total Worker Population Person"))
    cultivators = (_num(village_row.get("Main Cultivator Population Person")) + _num(village_row.get("Marginal Cultivator Population Person")))
    agri_labour = (_num(village_row.get("Main Agricultural Labourers Population Person")) + _num(village_row.get("Marginal Agriculture Labourers Population Person")))
    hh_industry = (_num(village_row.get("Main Household Industries Population Person")) + _num(village_row.get("Marginal Household Industries Population Person")))
    other_workers = (_num(village_row.get("Main Other Workers Population Person")) + _num(village_row.get("Marginal Other Workers Population Person")))

    f["population_norm"] = _safe_norm(pop, 5000)
    f["workers_norm"] = _safe_norm(workers, 3000)
    f["cultivators_norm"] = _safe_norm(cultivators, 1500)
    f["agri_labour_norm"] = _safe_norm(agri_labour, 2000)
    f["hh_industry_norm"] = _safe_norm(hh_industry, 200)
    f["other_workers_norm"] = _safe_norm(other_workers, 1500)

    f["veterinary_norm"] = _safe_norm(_num(village_row.get("Veterinary Hospital (Numbers)")), 1)
    f["govt_iti_norm"] = _safe_norm(_num(village_row.get("Govt Vocational Training School/ITI (Numbers)")), 1)
    f["private_iti_norm"] = _safe_norm(_num(village_row.get("Private Vocational Training School/ITI (Numbers)")), 1)
    f["market_norm"] = _safe_norm(_num(village_row.get("Mandis/Regular Market (Status A(1)/NA(2))")), 1)
    f["public_bus_norm"] = _safe_norm(_num(village_row.get("Public Bus Service (Status A(1)/NA(2))")), 1)
    f["private_bus_norm"] = _safe_norm(_num(village_row.get("Private Bus Service (Status A(1)/NA(2))")), 1)
    f["commercial_bank_norm"] = _safe_norm(_num(village_row.get("Commercial Bank (Status A(1)/NA(2))")), 1)
    f["coop_bank_norm"] = _safe_norm(_num(village_row.get("Cooperative Bank (Status A(1)/NA(2))")), 1)
    f["phc_norm"] = _safe_norm(_num(village_row.get("Primary Health Centre (Numbers)")), 1)
    f["chc_norm"] = _safe_norm(_num(village_row.get("Community Health Centre (Numbers)")), 1)
    f["govt_primary_school_norm"] = _safe_norm(_num(village_row.get("Govt Primary School (Numbers)")), 3)
    f["private_primary_school_norm"] = _safe_norm(_num(village_row.get("Private  Primary School (Numbers)")), 3)

    dairy = district_ctx.get("dairy") or {}
    f["dairy_district_norm"] = _safe_norm(_num(dairy.get("dairy_cooperative_societies")), 2000)

    ca = district_ctx.get("crop_area") or {}
    f["cultivated_area_norm"] = _safe_norm(_num(ca.get("total_cultivated_area")), 10_000_000)
    irrig = _num(ca.get("total_irrigated_area")); cult = _num(ca.get("total_cultivated_area"))
    f["irrigation_norm"] = (irrig / cult) if cult > 0 else 0.0

    cp = district_ctx.get("crop_production") or {}
    f["crop_production_norm"] = _safe_norm(_num(cp.get("total_production")), 500_000)

    f["transport"] = max(f["public_bus_norm"], f["private_bus_norm"])
    f["market"] = f["market_norm"]
    f["banks"] = max(f["commercial_bank_norm"], f["coop_bank_norm"])
    f["schools"] = max(f["govt_primary_school_norm"], f["private_primary_school_norm"])
    f["healthcare"] = max(f["phc_norm"], f["chc_norm"])
    f["population"] = f["population_norm"]
    f["workers"] = f["workers_norm"]
    f["cultivators"] = f["cultivators_norm"]
    f["agri_labour"] = f["agri_labour_norm"]
    f["agri_activity"] = max(f["cultivators_norm"], f["agri_labour_norm"])
    f["govt_iti"] = f["govt_iti_norm"]
    f["private_iti"] = f["private_iti_norm"]
    f["veterinary"] = f["veterinary_norm"]
    f["commercial_bank"] = f["commercial_bank_norm"]
    f["coop_bank"] = f["coop_bank_norm"]
    f["dairy_district"] = f["dairy_district_norm"]
    f["cultivated_area"] = f["cultivated_area_norm"]
    f["irrigation"] = f["irrigation_norm"]
    f["crop_production"] = f["crop_production_norm"]
    return f


def _weighted_score(features, weights):
    total_w = sum(weights.values()) or 1.0
    return float(sum((w / total_w) * features.get(k, 0.0) for k, w in weights.items()))


def compute_opportunity_scores(features, weights_cfg):
    return {cat: _weighted_score(features, w) for cat, w in weights_cfg.items()}


def generate_signals(village_row, district_ctx, features):
    signals = []

    if features["veterinary"] >= 0.5 and features["agri_activity"] >= 0.3 and features["transport"] >= 0.5:
        signals.append({"signal": "Dairy / Livestock opportunity signal detected",
            "evidence": "Veterinary support + agriculture activity + transport presence are relatively strong.",
            "related_business_category": "Dairy / Milk-related Business"})
    elif features["dairy_district"] > 0.2 and features["agri_activity"] >= 0.3:
        signals.append({"signal": "Dairy / Livestock opportunity signal detected (district context)",
            "evidence": "District shows notable dairy cooperative presence and village has agriculture activity.",
            "related_business_category": "Dairy / Milk-related Business"})

    if (features["cultivators"] >= 0.3 or features["agri_labour"] >= 0.3) and (features["crop_production"] >= 0.2 or features["cultivated_area"] >= 0.2) and features["market"] >= 0.5:
        signals.append({"signal": "Agri-processing opportunity signal detected",
            "evidence": "Cultivator / agri-labour population and crop context combined with market access.",
            "related_business_category": "Agri Processing"})

    if (features["govt_iti"] >= 0.5 or features["private_iti"] >= 0.5) and features["workers"] >= 0.25 and features["transport"] >= 0.5:
        signals.append({"signal": "Skill / repair service opportunity signal detected",
            "evidence": "ITI/vocational presence and worker population with transport availability.",
            "related_business_category": "Skill & Repair Services"})

    if features["population"] >= 0.3 and features["banks"] >= 0.5 and features["transport"] >= 0.5 and features["market"] >= 0.5:
        signals.append({"signal": "Rural service opportunity signal detected",
            "evidence": "Population, banks, transport and market support rural service businesses.",
            "related_business_category": "Rural Services"})

    if features["population"] >= 0.3 and features["market"] >= 0.5 and features["workers"] >= 0.25:
        signals.append({"signal": "Retail / trading opportunity signal detected",
            "evidence": "Population, market and worker base support retail and trading activities.",
            "related_business_category": "Retail & Trading"})

    return signals
