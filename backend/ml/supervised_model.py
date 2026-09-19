"""Random Forest PROXY supervised model."""

from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from config import AMENITY_FEATURES, RANDOM_STATE


def build_proxy_features(df):
    cols = [c for c in AMENITY_FEATURES if c in df.columns]
    X = df[cols].copy()
    if "cluster" in df.columns: X["cluster"] = df["cluster"].values
    return X.values.astype(float)


def train_proxy_rf(village_df, opportunity_scores_per_village):
    X = build_proxy_features(village_df)
    cat_cols = list(opportunity_scores_per_village.columns)
    labels = opportunity_scores_per_village[cat_cols].idxmax(axis=1)
    mask = ~np.isnan(X).all(axis=1)
    X = X[mask]; labels = labels[mask]

    if len(X) < 5:
        le = LabelEncoder().fit(cat_cols)
        y = le.transform(labels)
        clf = RandomForestClassifier(n_estimators=10, random_state=RANDOM_STATE)
        X2 = np.vstack([X] * 5) if len(X) else np.zeros((5, len(build_proxy_features(village_df)[0])))
        y2 = np.resize(y, len(X2))
        clf.fit(X2, y2)
    else:
        le = LabelEncoder().fit(cat_cols)
        y = le.transform(labels)
        clf = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1)
        clf.fit(X, y)

    return {"model": clf, "label_encoder": le, "feature_names": list(
        [c for c in AMENITY_FEATURES if c in village_df.columns] + (["cluster"] if "cluster" in village_df.columns else []))}


def predict_proxy(artifacts, village_row):
    le = artifacts["label_encoder"]; model = artifacts["model"]
    cols = [c for c in AMENITY_FEATURES if c in village_row.index]
    x = village_row[cols].values.astype(float)
    if "cluster" in village_row.index and "cluster" in artifacts["feature_names"]:
        x = np.concatenate([x, [float(village_row["cluster"])]])
    x = x.reshape(1, -1)
    x = np.nan_to_num(x, nan=0.0)
    proba = model.predict_proba(x)[0]
    idx = int(np.argmax(proba))
    pred_label = le.inverse_transform([idx])[0]
    confidence = float(proba[idx])
    return {"predicted_category": pred_label, "confidence": round(confidence, 4),
            "disclaimer": "Random Forest Proxy Prediction - prototype supervised model trained using proxy labels. Not a predictor of real-world business success."}
