"""
Step 3 + 4: SHAP Explainability + FastAPI Backend
Run: uvicorn api:app --reload --port 8000
"""

import pickle
import numpy as np
import pandas as pd
import shap
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from rag import get_recommendation

# ── Load model & metadata ──────────────────────────────────────────────────────
with open("models/best_model.pkl", "rb") as f:
    MODEL = pickle.load(f)

with open("models/model_meta.pkl", "rb") as f:
    META = pickle.load(f)

FEATURE_NAMES: List[str] = META["feature_names"]

# ── SHAP explainer (TreeExplainer for RF/XGB, LinearExplainer for LR) ─────────
def _build_explainer(model):
    try:
        return shap.TreeExplainer(model)
    except Exception:
        return shap.LinearExplainer(model, np.zeros((1, len(FEATURE_NAMES))))

EXPLAINER = _build_explainer(MODEL)


# def get_top_factors(feature_values: pd.DataFrame, n: int = 3) -> List[str]:
#     """Return top-n feature names by absolute SHAP value."""
#     shap_vals = EXPLAINER.shap_values(feature_values)
#     # For binary classifiers shap_values may return list [class0, class1]
#     if isinstance(shap_vals, list):
#         shap_vals = shap_vals[1]
#     importances = np.abs(shap_vals[0])
#     top_idx = np.argsort(importances)[::-1][:n]
#     return [FEATURE_NAMES[i] for i in top_idx]
def get_top_factors(feature_values: pd.DataFrame, n: int = 3) -> List[str]:
    """Return top-n feature names by absolute SHAP value (robust version)."""
    
    shap_vals = EXPLAINER.shap_values(feature_values)

    # Case 1: Tree models → list of arrays [class0, class1]
    if isinstance(shap_vals, list):
        shap_vals = shap_vals[1]

    # Case 2: Ensure numpy array
    shap_vals = np.array(shap_vals)

    # Case 3: Flatten properly (important fix)
    if shap_vals.ndim == 3:
        shap_vals = shap_vals[0]

    # Now safe
    importances = np.abs(shap_vals[0])

    top_idx = np.argsort(importances)[::-1][:n]
    print("SHAP SHAPE:", shap_vals.shape)
    print("IMPORTANCES:", importances[:5])

    return [FEATURE_NAMES[int(i)] for i in top_idx]


# ── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI(title="Student Dropout Prediction API")


class StudentFeatures(BaseModel):
    # Core required fields — all others default to 0
    school:     int = 0
    sex:        int = 0
    age:        int = 17
    address:    int = 0
    famsize:    int = 0
    Pstatus:    int = 0
    Medu:       int = 2
    Fedu:       int = 2
    Mjob:       int = 0
    Fjob:       int = 0
    reason:     int = 0
    guardian:   int = 0
    traveltime: int = 1
    studytime:  int = 2
    failures:   int = 0
    schoolsup:  int = 0
    famsup:     int = 0
    paid:       int = 0
    activities: int = 0
    nursery:    int = 0
    higher:     int = 1
    internet:   int = 1
    romantic:   int = 0
    famrel:     int = 3
    freetime:   int = 3
    goout:      int = 2
    Dalc:       int = 1
    Walc:       int = 1
    health:     int = 3
    absences:   int = 0
    G1:         float = 10.0
    G2:         float = 10.0
    G3:         float = 10.0
    engagement_score: float = 0.0
    academic_risk:    float = 10.0

    class Config:
        extra = "allow"   # accept extra fields from future dataset versions


@app.get("/")
def root():
    return {"status": "ok", "model": META["best_model_name"]}


@app.post("/predict")
def predict(student: StudentFeatures) -> Dict[str, Any]:
    try:
        # Build feature dict using model's expected feature order
        data = student.dict()
        row = {feat: data.get(feat, 0) for feat in FEATURE_NAMES}
        df_input = pd.DataFrame([row])

        # Risk score = P(dropout=1)
        if hasattr(MODEL, "predict_proba"):
            proba = MODEL.predict_proba(df_input)[0]
            risk_score = float(proba[1])
        else:
            risk_score = float(MODEL.predict(df_input)[0])

        # Risk level
        if risk_score < 0.4:
            risk_level = "Low"
        elif risk_score <= 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"

        # Top SHAP factors
        top_factors = get_top_factors(df_input)

        # RAG recommendation
        recommendation = get_recommendation(top_factors, risk_level)

        return {
            "risk_score":      round(risk_score, 4),
            "risk_level":      risk_level,
            "top_factors":     top_factors,
            "recommendation":  recommendation,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
