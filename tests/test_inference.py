from backend.ml.inference import ChurnPredictor

def test_fallback_predictor_returns_probability(settings, tmp_path):
    settings.ML_ARTIFACT_DIR = tmp_path
    result = ChurnPredictor().predict({"contract": "Month-to-month", "monthly_charges": 90, "tenure": 2, "tech_support": "No"})
    assert 0 <= result["churn_probability"] <= 1
    assert result["risk_level"] in {"low", "medium", "high"}

