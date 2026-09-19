"""K-Means clustering."""

from __future__ import annotations
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from config import AMENITY_FEATURES, AMENITY_LABELS, RANDOM_STATE


def train_kmeans(df):
    X_raw = df[AMENITY_FEATURES].copy()
    imputer = SimpleImputer(strategy="median")
    X_imp = imputer.fit_transform(X_raw)
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X_imp)

    best_k = 2; best_score = -1.0; scores = {}
    max_k = min(6, max(2, len(X_std) - 1))
    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = km.fit_predict(X_std)
        if len(set(labels)) < 2: continue
        try: s = silhouette_score(X_std, labels)
        except Exception: s = -1.0
        scores[k] = float(s)
        if s > best_score: best_score = s; best_k = k

    final = KMeans(n_clusters=best_k, random_state=RANDOM_STATE, n_init=10)
    labels = final.fit_predict(X_std)
    df_out = df.copy(); df_out["cluster"] = labels

    profiles = []
    for cid in sorted(set(labels)):
        sub = df_out[df_out["cluster"] == cid]
        means = {f: float(np.nanmean(sub[f].astype(float))) if f in sub else float("nan") for f in AMENITY_FEATURES}
        valid = {k: v for k, v in means.items() if not np.isnan(v)}
        strongest = sorted(valid.items(), key=lambda x: -x[1])[:3] if valid else []
        weakest = sorted(valid.items(), key=lambda x: x[1])[:3] if valid else []
        profiles.append({
            "cluster_id": int(cid), "size": int(len(sub)), "means": means,
            "strongest_features": [{"feature": AMENITY_LABELS.get(f, f), "value": round(v, 2)} for f, v in strongest],
            "weakest_features": [{"feature": AMENITY_LABELS.get(f, f), "value": round(v, 2)} for f, v in weakest],
            "description": _describe_cluster(strongest, weakest),
        })

    return {"model": final, "imputer": imputer, "scaler": scaler, "k": best_k,
            "silhouette": best_score, "silhouette_scores": scores, "labels": labels,
            "village_index": df_out, "cluster_profiles": profiles}


def _describe_cluster(strongest, weakest):
    if not strongest: return "Cluster profile could not be computed from available data."
    strong_names = ", ".join(AMENITY_LABELS.get(f, f) for f, _ in strongest)
    weak_names = ", ".join(AMENITY_LABELS.get(f, f) for f, _ in weakest) if weakest else "-"
    return (f"Villages in this cluster show relatively higher values in: {strong_names}. "
            f"Relatively lower presence in: {weak_names}.")


def assign_cluster(village_row, artifacts):
    x = village_row[AMENITY_FEATURES].values.reshape(1, -1).astype(float)
    x_imp = artifacts["imputer"].transform(x)
    x_std = artifacts["scaler"].transform(x_imp)
    cid = int(artifacts["model"].predict(x_std)[0])
    profile = next((p for p in artifacts["cluster_profiles"] if p["cluster_id"] == cid), None)
    return {"cluster_id": cid, "k": artifacts["k"],
            "silhouette": round(float(artifacts["silhouette"]), 4), "cluster_profile": profile}
