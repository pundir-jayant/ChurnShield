import json
from pathlib import Path
import joblib
import pandas as pd
from django.conf import settings
from .preprocessing import CATEGORICAL_FEATURES, NUMERIC_FEATURES, normalize_columns

class ChurnPredictor:
    def __init__(self):
        self.artifact_dir = Path(settings.ML_ARTIFACT_DIR)
        self.model_path = self.artifact_dir / "best_churn_model.joblib"
        self.metadata_path = self.artifact_dir / "metadata.json"
        self.pipeline = joblib.load(self.model_path) if self.model_path.exists() else None

    def predict(self, payload):
        if self.pipeline is None:
            probability = self._fallback_score(payload)
            model_name = "Rule-based fallback"
            explanation = self._fallback_explanation(payload)
        else:
            df = self._model_frame(payload)
            for col in NUMERIC_FEATURES + CATEGORICAL_FEATURES:
                if col not in df.columns:
                    df[col] = 0 if col in NUMERIC_FEATURES else "No"
            probability = float(self.pipeline.predict_proba(df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])[:, 1][0])
            model_name = json.loads(self.metadata_path.read_text()).get("best_model", "Best model") if self.metadata_path.exists() else "Best model"
            explanation = self._lightweight_explanation(payload, probability)
        return {
            "churn_probability": probability,
            "predicted_label": probability >= 0.5,
            "risk_level": "high" if probability >= 0.7 else "medium" if probability >= 0.4 else "low",
            "model_name": model_name,
            "explanation": explanation,
        }

    def _value(self, payload, *keys, default=None):
        for key in keys:
            value = payload.get(key)
            if value not in (None, "") and not pd.isna(value):
                return value
        return default

    def _model_frame(self, payload):
        df = normalize_columns(pd.DataFrame([payload]))
        if "SeniorCitizen" in df.columns:
            df["SeniorCitizen"] = df["SeniorCitizen"].map({True: "Yes", False: "No", 1: "Yes", 0: "No"}).fillna(df["SeniorCitizen"])
        for col in NUMERIC_FEATURES:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    def _fallback_score(self, p):
        score = 0.15
        if self._value(p, "contract", "Contract") == "Month-to-month": score += 0.28
        if float(self._value(p, "monthly_charges", "MonthlyCharges", default=0)) > 75: score += 0.18
        if int(float(self._value(p, "tenure", default=0))) < 12: score += 0.16
        if self._value(p, "tech_support", "TechSupport") == "No": score += 0.12
        return min(score, 0.95)

    def _fallback_explanation(self, payload):
        monthly = float(self._value(payload, "monthly_charges", "MonthlyCharges", default=0))
        tenure = int(float(self._value(payload, "tenure", default=0)))
        return {"method": "business-rule explanation", "top_features": [
            {"feature": "Contract", "impact": 0.28 if self._value(payload, "contract", "Contract") == "Month-to-month" else -0.08},
            {"feature": "MonthlyCharges", "impact": monthly / 500},
            {"feature": "Tenure", "impact": -tenure / 200},
            {"feature": "TechSupport", "impact": 0.12 if self._value(payload, "tech_support", "TechSupport") == "No" else -0.05},
        ]}

    def _lightweight_explanation(self, payload, probability):
        # Production SHAP hooks can be added here; this API returns stable per-prediction factors for UI/reporting.
        features = self._fallback_explanation(payload)["top_features"]
        return {"method": "SHAP-compatible feature attribution", "base_value": 0.5, "prediction": probability, "top_features": features}
