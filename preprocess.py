"""
Step 1: Data Preprocessing
Run: python preprocess.py --input data/student-mat.csv
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import os

def preprocess(input_path: str, output_path: str = "data/processed.csv"):
    # ── Load ──────────────────────────────────────────────────────────────────
    df = pd.read_csv(input_path, sep=",")
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    # ── Handle missing values ──────────────────────────────────────────────────
    for col in df.columns:
        if df[col].dtype in [np.float64, np.int64]:
            df[col].fillna(df[col].mean(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0], inplace=True)

    # ── Encode categorical columns ─────────────────────────────────────────────
    le = LabelEncoder()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col].astype(str))
    print(f"Encoded {len(categorical_cols)} categorical columns: {categorical_cols}")

    # ── Feature Engineering ────────────────────────────────────────────────────
    df["engagement_score"] = df["studytime"] * 2 - df["absences"]
    df["academic_risk"]    = df["failures"] + (20 - df["G3"])

    # ── Target column ─────────────────────────────────────────────────────────
    df["dropout"] = (
        (df["G3"] < 10) & ((df["absences"] > 10) | (df["failures"] > 0))
    ).astype(int)
    print(f"Dropout distribution:\n{df['dropout'].value_counts()}")

    # ── Normalize numerical features (excluding target + engineered) ───────────
    exclude = {"dropout", "engagement_score", "academic_risk"}
    num_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c not in exclude]
    scaler = MinMaxScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    # ── Save ───────────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved processed dataset → {output_path}")
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="data/student-mat.csv")
    parser.add_argument("--output", default="data/processed.csv")
    args = parser.parse_args()
    preprocess(args.input, args.output)
