"""
Train all models and save artifacts.

© 2026 Code Ninjas (SIH 2026, PS26091)
All Rights Reserved.
"""

from __future__ import annotations
import json
import joblib
import pandas as pd

from config import AMENITY_FEATURES, MODEL_DIR, OPPORTUNITY_WEIGHTS
from data_loader import build_village_master, get_district_context
from ml.clustering import train_kmeans
from ml.opportunity_gap import compute_raw_features, compute_opportunity_scores
from ml.supervised_model import train_proxy_rf


def main():
    print("Loading village master...")
    vdf = build_village_master()
    print(f"  -> {len(vdf)} village rows")

    print("Training K-Means...")
    km_art = train_kmeans(vdf)
    print(f"  -> best K = {km_art['k']}, silhouette = {km_art['silhouette']:.4f}")

    village_df = km_art["village_index"].copy()

    joblib.dump(km_art["model"], MODEL_DIR / "kmeans_model.pkl")
    joblib.dump(km_art["imputer"], MODEL_DIR / "imputer.pkl")
    joblib.dump(km_art["scaler"], MODEL_DIR / "scaler.pkl")
    joblib.dump({"k": km_art["k"], "silhouette": km_art["silhouette"],
                 "silhouette_scores": km_art["silhouette_scores"],
                 "cluster_profiles": km_art["cluster_profiles"],
                 "amenity_features": AMENITY_FEATURES}, MODEL_DIR / "feature_config.pkl")
    joblib.dump(km_art["cluster_profiles"], MODEL_DIR / "cluster_profiles.pkl")

    print("Computing opportunity scores (proxy labels)...")
    districts_cache = {}
    rows = []
    for _, row in village_df.iterrows():
        d = row["District_Name"]
        if d not in districts_cache: districts_cache[d] = get_district_context(d)
        feats = compute_raw_features(row, districts_cache[d])
        rows.append(compute_opportunity_scores(feats, OPPORTUNITY_WEIGHTS))
    scores_df = pd.DataFrame(rows, index=village_df.index)

    print("Training Random Forest proxy model...")
    rf_art = train_proxy_rf(village_df, scores_df)
    joblib.dump(rf_art, MODEL_DIR / "random_forest_model.pkl")

    village_df.drop(columns=[c for c in village_df.columns if c.startswith("_")], inplace=True)
    village_df.to_csv(MODEL_DIR / "village_master_snapshot.csv", index=False)

    meta = {"k": km_art["k"], "silhouette": km_art["silhouette"],
            "num_villages": int(len(village_df)), "categories": list(OPPORTUNITY_WEIGHTS.keys())}
    with open(MODEL_DIR / "meta.json", "w") as fh: json.dump(meta, fh, indent=2)

    print("Done. Artifacts saved in", MODEL_DIR)


if __name__ == "__main__":
    main()
