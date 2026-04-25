"""
Step 2: Model Training
Run: python train.py
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score
from xgboost import XGBClassifier

DATA_PATH  = "data/processed.csv"
MODEL_PATH = "models/best_model.pkl"
META_PATH  = "models/model_meta.pkl"

def train():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["dropout"])
    y = df["dropout"]
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest":       RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost":            XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
    }

    results = {}
    trained = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            "accuracy": accuracy_score(y_test, y_pred),
            "f1":       f1_score(y_test, y_pred, zero_division=0),
            "recall":   recall_score(y_test, y_pred, zero_division=0),
        }
        trained[name] = model
        print(f"{name:25s} | acc={results[name]['accuracy']:.3f} | "
              f"f1={results[name]['f1']:.3f} | recall={results[name]['recall']:.3f}")

    # Select best by recall
    best_name = max(results, key=lambda k: results[k]["recall"])
    best_model = trained[best_name]
    print(f"\n✅ Best model (by recall): {best_name}")

    os.makedirs("models", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(best_model, f)

    # meta = {"feature_names": list(X.columns), "best_model_name": best_name}
    meta = {
    "feature_names": list(X.columns),
    "best_model_name": best_name,
    "metrics": results
}
    with open(META_PATH, "wb") as f:
        pickle.dump(meta, f)

    print(f"Model saved → {MODEL_PATH}")
    print(f"Meta  saved → {META_PATH}")
    return best_model, meta

if __name__ == "__main__":
    train()
