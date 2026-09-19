"""Loads datasets and exposes clean APIs. Granularity rule is strict."""

from __future__ import annotations
import re
from functools import lru_cache
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from config import AMENITY_FEATURES, DATA_DIR, FILES, SUPPORTED_DISTRICTS


def _normalize_text(s):
    if pd.isna(s): return ""
    s = str(s).strip()
    return re.sub(r"\s+", " ", s)


def _normalize_key(s):
    if pd.isna(s): return ""
    s = str(s).lower()
    s = re.sub(r"[\(\)\[\]\{\}\.,'\"\-_/]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _to_number(series): return pd.to_numeric(series, errors="coerce")


@lru_cache(maxsize=1)
def load_pca_villages():
    df = pd.read_csv(DATA_DIR / FILES["pca_villages"])
    df["District_Name"] = df["District_Name"].astype(str).str.strip()
    df["Level"] = df["Level"].astype(str).str.strip()
    df["Name"] = df["Name"].astype(str).apply(_normalize_text)
    df["_district_key"] = df["District_Name"].apply(_normalize_key)
    df["_village_key"] = df["Name"].apply(_normalize_key)
    num_cols = ["No of Households","Total Population Person","Total Worker Population Person",
                "Main Cultivator Population Person","Main Agricultural Labourers Population Person",
                "Main Household Industries Population Person","Main Other Workers Population Person",
                "Marginal Cultivator Population Person","Marginal Agriculture Labourers Population Person",
                "Marginal Household Industries Population Person","Marginal Other Workers Population Person",
                "Non Working Population Person"]
    for c in num_cols:
        if c in df.columns: df[c] = _to_number(df[c])
    return df


@lru_cache(maxsize=1)
def load_village_clustering():
    df = pd.read_csv(DATA_DIR / FILES["village_clustering"])
    df["District Name"] = df["District Name"].astype(str).str.strip()
    df["Village Name"] = df["Village Name"].astype(str).apply(_normalize_text)
    df["_district_key"] = df["District Name"].apply(_normalize_key)
    df["_village_key"] = df["Village Name"].apply(_normalize_key)
    for c in AMENITY_FEATURES:
        if c in df.columns: df[c] = _to_number(df[c])
    return df


@lru_cache(maxsize=1)
def load_b04():
    df = pd.read_csv(DATA_DIR / FILES["b04"])
    if "district" in df.columns: df["district"] = df["district"].astype(str).str.strip()
    return df


@lru_cache(maxsize=1)
def load_b24():
    df = pd.read_csv(DATA_DIR / FILES["b24"])
    if "district" in df.columns: df["district"] = df["district"].astype(str).str.strip()
    return df


@lru_cache(maxsize=1)
def load_crop_area():
    df = pd.read_csv(DATA_DIR / FILES["crop_area"])
    df["district"] = df["district"].astype(str).str.strip()
    return df


@lru_cache(maxsize=1)
def load_crop_production():
    df = pd.read_csv(DATA_DIR / FILES["crop_production"])
    col = "district_district" if "district_district" in df.columns else df.columns[0]
    df = df.rename(columns={col: "district"})
    df["district"] = df["district"].astype(str).str.strip()
    return df


@lru_cache(maxsize=1)
def load_dairy():
    df = pd.read_csv(DATA_DIR / FILES["dairy"])
    df["district"] = df["district"].astype(str).str.strip()
    return df


@lru_cache(maxsize=1)
def load_village_amenities_district():
    df = pd.read_csv(DATA_DIR / FILES["village_amenities_district"])
    df["District Name"] = df["District Name"].astype(str).str.strip()
    return df


@lru_cache(maxsize=1)
def build_village_master():
    pca = load_pca_villages()
    pca_v = pca[pca["Level"].str.upper() == "VILLAGE"].copy()
    clust = load_village_clustering()
    merged = pca_v.merge(clust, on=["_district_key","_village_key"], how="left", suffixes=("","_clust"))
    merged["District_Name"] = merged["District_Name"].fillna("")
    merged["Name"] = merged["Name"].fillna("")
    for c in AMENITY_FEATURES:
        if c not in merged.columns: merged[c] = np.nan
    return merged


def list_districts(): return list(SUPPORTED_DISTRICTS)


def list_villages(district):
    d_key = _normalize_key(district)
    df = build_village_master()
    sub = df[df["_district_key"] == d_key]
    if "Village Name" in sub.columns:
        sub = sub[sub["Village Name"].notna()]
    return sorted({_normalize_text(n) for n in sub["Name"].tolist() if _normalize_text(n)})


def find_village(district, village):
    d_key = _normalize_key(district); v_key = _normalize_key(village)
    df = build_village_master()
    sub = df[(df["_district_key"] == d_key) & (df["_village_key"] == v_key)]
    if sub.empty: return None
    return sub.iloc[0]


def get_district_context(district):
    d = district.strip()
    out = {"district": d, "sources": {}}

    try:
        b04 = load_b04()
        row = b04[b04["district"].str.lower() == d.lower()]
        if not row.empty:
            r = row.iloc[0]
            out["workforce"] = {"cultivators_pct": float(r.get("cultivators_pct")),
                                "agricultural_labourers_pct": float(r.get("agricultural_labourers_pct")),
                                "category_B_pct": float(r.get("category_B_pct")),
                                "category_C_HHI_pct": float(r.get("category_C_HHI_pct"))}
            out["sources"]["workforce"] = "Census B-04 (district-level)"
        else: out["workforce"] = None
    except Exception: out["workforce"] = None

    try:
        b24 = load_b24()
        row = b24[b24["district"].str.lower() == d.lower()]
        if not row.empty:
            r = row.iloc[0]
            out["occupation"] = {k: float(v) for k, v in r.items() if k != "district"}
            out["sources"]["occupation"] = "Census B-24 (district-level)"
        else: out["occupation"] = None
    except Exception: out["occupation"] = None

    try:
        ca = load_crop_area()
        row = ca[ca["district"].str.lower() == d.lower()]
        if not row.empty:
            r = row.iloc[0]
            out["crop_area"] = {"total_cultivated_area": float(r.get("total_cultivated_area")),
                                "total_irrigated_area": float(r.get("total_irrigated_area")),
                                "food_grain_area": float(r.get("food_grain_area")),
                                "food_grain_irrigated_area": float(r.get("food_grain_irrigated_area"))}
            out["sources"]["crop_area"] = "Crop Area dataset (district-level)"
        else: out["crop_area"] = None
    except Exception: out["crop_area"] = None

    try:
        cp = load_crop_production()
        row = cp[cp["district"].str.lower() == d.lower()]
        if not row.empty:
            r = row.iloc[0]
            out["crop_production"] = {"cereals_all": float(r.get("cereals_all") or 0),
                                      "pulses_all": float(r.get("pulses_all") or 0),
                                      "total_production": float(r.get("total_production") or 0),
                                      "cereals_all_pct": float(r.get("cereals_all_pct") or 0),
                                      "pulses_all_pct": float(r.get("pulses_all_pct") or 0)}
            out["sources"]["crop_production"] = "Crop Production dataset (district-level)"
        else: out["crop_production"] = None
    except Exception: out["crop_production"] = None

    try:
        dr = load_dairy()
        row = dr[dr["district"].str.lower() == d.lower()]
        if not row.empty:
            r = row.iloc[0]
            out["dairy"] = {"dairy_cooperative_societies": int(r.get("dairy_cooperative_societies") or 0),
                            "total_members": int(r.get("total_members") or 0),
                            "milk_collected_000_litre": float(r.get("milk_collected_000_litre") or 0),
                            "daily_average_000_litre": float(r.get("daily_average_000_litre") or 0),
                            "cold_storages": int(r.get("cold_storages") or 0),
                            "cold_storage_capacity_000_litre": float(r.get("cold_storage_capacity_000_litre") or 0)}
            out["sources"]["dairy"] = "Dairy Development 2010-11 (district-level)"
        else: out["dairy"] = None
    except Exception: out["dairy"] = None

    return out


def district_has_context(district):
    ctx = get_district_context(district)
    return {k: ctx.get(k) is not None for k in ["workforce","occupation","crop_area","crop_production","dairy"]}
