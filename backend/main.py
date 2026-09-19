"""
FastAPI backend for Rural Business Advisor.

© 2026 Code Ninjas (SIH 2026, PS26091)
All Rights Reserved.
"""

from __future__ import annotations
from typing import Any, Dict, Optional
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import (AMENITY_FEATURES, AMENITY_LABELS, BUSINESS_CATALOG, MODEL_DIR,
                    OPPORTUNITY_WEIGHTS, SUPPORTED_DISTRICTS)
from data_loader import find_village, get_district_context, list_villages, list_districts
from ml.clustering import assign_cluster
from ml.opportunity_gap import compute_opportunity_scores, compute_raw_features, generate_signals
from ml.recommendation import build_recommendations
from ml.supervised_model import predict_proxy
from services.financial import financial_analysis, what_if_analysis
from services.schemes import pmegp_relevance
from services.llm_service import generate_advice, is_llm_available
from services.db_service import save_report, get_history, get_analytics, is_db_available

app = FastAPI(title="Rural Business Advisor API")

app.add_middleware(CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
    ],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

ARTIFACTS: Dict[str, Any] = {}


def _load_artifacts():
    try:
        ARTIFACTS["kmeans"] = joblib.load(MODEL_DIR / "kmeans_model.pkl")
        ARTIFACTS["imputer"] = joblib.load(MODEL_DIR / "imputer.pkl")
        ARTIFACTS["scaler"] = joblib.load(MODEL_DIR / "scaler.pkl")
        ARTIFACTS["feature_config"] = joblib.load(MODEL_DIR / "feature_config.pkl")
        ARTIFACTS["cluster_profiles"] = joblib.load(MODEL_DIR / "cluster_profiles.pkl")
        ARTIFACTS["rf"] = joblib.load(MODEL_DIR / "random_forest_model.pkl")
    except Exception as exc:
        print("WARNING: missing artifacts. Run `python train.py` first.", exc)


@app.on_event("startup")
def startup_event():
    _load_artifacts()


class RecommendRequest(BaseModel):
    district: str
    village: str
    budget: float = Field(..., gt=0)
    name: Optional[str] = None
    language: Optional[str] = "en"   # 🆕 "hi", "en", "mr"


class FinancialRequest(BaseModel):
    initial_investment: float = Field(..., gt=0)
    selling_price_per_unit: float = Field(..., ge=0)
    units_per_month: float = Field(..., ge=0)
    monthly_fixed_cost: float = Field(..., ge=0)
    variable_cost_per_unit: float = Field(..., ge=0)


class WhatIfRequest(FinancialRequest):
    pass


@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": bool(ARTIFACTS.get("rf"))}


@app.get("/districts")
def districts():
    return {"districts": list_districts()}


@app.get("/villages/{district}")
def villages(district: str):
    if district not in SUPPORTED_DISTRICTS:
        raise HTTPException(status_code=400, detail=f"Unsupported district: {district}")
    return {"district": district, "villages": list_villages(district)}


@app.get("/cluster-profile")
def cluster_profile():
    if "feature_config" not in ARTIFACTS:
        raise HTTPException(status_code=503, detail="Models not trained. Run train.py.")
    cfg = ARTIFACTS["feature_config"]
    return {"k": cfg["k"], "silhouette": cfg["silhouette"],
            "silhouette_scores": cfg["silhouette_scores"],
            "cluster_profiles": cfg["cluster_profiles"]}


def _build_cluster_artifacts():
    return {"model": ARTIFACTS["kmeans"], "imputer": ARTIFACTS["imputer"],
            "scaler": ARTIFACTS["scaler"], "k": ARTIFACTS["feature_config"]["k"],
            "silhouette": ARTIFACTS["feature_config"]["silhouette"],
            "cluster_profiles": ARTIFACTS["cluster_profiles"]}


@app.post("/recommend")
def recommend(req: RecommendRequest):
    if req.district not in SUPPORTED_DISTRICTS:
        raise HTTPException(status_code=400, detail=f"Unsupported district: {req.district}")
    row = find_village(req.district, req.village)
    if row is None:
        raise HTTPException(status_code=404,
                            detail=f"Village '{req.village}' not found in district '{req.district}'.")
    if "feature_config" not in ARTIFACTS:
        raise HTTPException(status_code=503, detail="Models not trained. Run train.py.")

    village_profile = {
        "district": req.district, "village": str(row["Name"]),
        "population": _num_or_none(row.get("Total Population Person")),
        "households": _num_or_none(row.get("No of Households")),
        "total_workers": _num_or_none(row.get("Total Worker Population Person")),
        "main_cultivators": _num_or_none(row.get("Main Cultivator Population Person")),
        "main_agri_labourers": _num_or_none(row.get("Main Agricultural Labourers Population Person")),
        "main_hh_industry": _num_or_none(row.get("Main Household Industries Population Person")),
        "main_other_workers": _num_or_none(row.get("Main Other Workers Population Person")),
        "marginal_cultivators": _num_or_none(row.get("Marginal Cultivator Population Person")),
        "marginal_agri_labourers": _num_or_none(row.get("Marginal Agriculture Labourers Population Person")),
        "marginal_hh_industry": _num_or_none(row.get("Marginal Household Industries Population Person")),
        "marginal_other_workers": _num_or_none(row.get("Marginal Other Workers Population Person")),
        "non_workers": _num_or_none(row.get("Non Working Population Person")),
        "level": "Village-level data",
    }

    infrastructure = {}
    for feat in AMENITY_FEATURES:
        v = row.get(feat, np.nan)
        infrastructure[AMENITY_LABELS.get(feat, feat)] = None if pd.isna(v) else float(v)

    cluster_info = assign_cluster(row, _build_cluster_artifacts())
    cluster_info["size"] = next(
        (p["size"] for p in ARTIFACTS["cluster_profiles"]
         if p["cluster_id"] == cluster_info["cluster_id"]), None)

    district_ctx = get_district_context(req.district)
    feats = compute_raw_features(row, district_ctx)
    signals = generate_signals(row, district_ctx, feats)
    opportunity_scores = compute_opportunity_scores(feats, OPPORTUNITY_WEIGHTS)
    recommendations = build_recommendations(opportunity_scores, feats,
                                            budget=req.budget, signals=signals)

    row_with_cluster = row.copy()
    row_with_cluster["cluster"] = cluster_info["cluster_id"]
    rf_pred = predict_proxy(ARTIFACTS["rf"], row_with_cluster)

    top = recommendations[0] if recommendations else None
    required = top["estimated_investment"] if top else 0.0
    funding_gap = max(required - req.budget, 0.0)
    budget_analysis = {"user_budget": req.budget,
                       "top_recommendation_required_investment": required,
                       "funding_gap": round(funding_gap, 2)}

    pmegp = pmegp_relevance(req.budget, funding_gap)
    # ---------- LLM (Groq) enhancement ----------
    llm_advice = None
    if is_llm_available():
        try:
            top_biz_for_llm = []
            for rec in recommendations[:4]:
                sub_name = rec["sub_business"]
                cost = rec["estimated_investment"]
                rev = int(cost * 0.35)
                prof = int(cost * 0.10)
                roi = int((prof * 12 / cost) * 100) if cost else 0
                top_biz_for_llm.append({
                    "n": sub_name,
                    "cost": cost,
                    "rev": rev,
                    "profit": prof,
                    "roi": roi,
                })

            crops_ctx = "mixed crops"
            if district_ctx.get("crop_production"):
                cp = district_ctx["crop_production"]
                crops_ctx = f"Cereals: {cp.get('cereals_all', 0)}, Pulses: {cp.get('pulses_all', 0)}"
            elif district_ctx.get("crop_area"):
                ca = district_ctx["crop_area"]
                crops_ctx = f"Cultivated area: {ca.get('total_cultivated_area', 0)}"

            llm_advice = generate_advice(
                village=village_profile["village"],
                taluka=req.district,
                district=req.district,
                population=village_profile.get("population"),
                crops=crops_ctx,
                region="Maharashtra",
                capital=int(req.budget),
                category=recommendations[0]["business_category"] if recommendations else "general",
                experience="user-specified",
                businesses=top_biz_for_llm,
                language=(req.language or "en"),
            )
        except Exception as e:
            print(f"[recommend] LLM enhancement failed: {e}")
            llm_advice = None

    # ---------- Save to MongoDB ----------
    saved_id = None
    try:
        report_to_save = {
            "name": req.name or "",
            "district": req.district,
            "village": req.village,
            "budget": req.budget,
            "category": recommendations[0]["business_category"] if recommendations else "",
            "cluster_id": cluster_info.get("cluster_id"),
            "ml_prediction": rf_pred,
            "recommendations": recommendations[:4],
        }
        saved_id = save_report(report_to_save)
    except Exception as e:
        print(f"[recommend] DB save failed: {e}")
        saved_id = None

    return {"village": village_profile, "infrastructure": infrastructure,
            "cluster": cluster_info, "economic_context": district_ctx,
            "opportunity_signals": signals, "opportunity_scores": opportunity_scores,
            "business_recommendations": recommendations, "ml_prediction": rf_pred,
            "budget_analysis": budget_analysis, "pmegp": pmegp,
            "llm_advice": llm_advice,
            "report_id": saved_id,
            "llm_available": is_llm_available(),
            "db_available": is_db_available(),
             "language": req.language or "en",
            "business_catalog": BUSINESS_CATALOG,
            "limitations": [
                "K-Means identifies similar village profiles - it does not prove market demand.",
                "Opportunity signals are derived from available data - not proof of demand.",
                "No genuine village-level historical business success labels exist.",
                "Random Forest is trained on proxy labels.",
                "Financial calculations depend on user assumptions.",
                "Startup costs are prototype/domain estimates.",
                "Government scheme details must be verified officially.",
                "Some datasets are district-level context, not village-level data.",
                "Missing data is never fabricated.",
            ]}

@app.get("/llm-status")
def llm_status():
    return {
        "llm_available": is_llm_available(),
        "db_available": is_db_available(),
    }


@app.get("/history")
def history(limit: int = 20):
    return {"reports": get_history(limit)}


@app.get("/analytics")
def analytics():
    return get_analytics()
@app.post("/financial-analysis")
def financial(req: FinancialRequest):
    return financial_analysis(req.initial_investment, req.selling_price_per_unit,
                              req.units_per_month, req.monthly_fixed_cost,
                              req.variable_cost_per_unit)


@app.post("/what-if")
def what_if(req: WhatIfRequest):
    return what_if_analysis({"initial_investment": req.initial_investment,
                             "selling_price_per_unit": req.selling_price_per_unit,
                             "units_per_month": req.units_per_month,
                             "monthly_fixed_cost": req.monthly_fixed_cost,
                             "variable_cost_per_unit": req.variable_cost_per_unit})


def _num_or_none(v):
    try:
        if v is None or pd.isna(v):
            return None
        return float(v)
    except Exception:
        return None