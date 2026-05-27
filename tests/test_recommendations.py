from backend.recommendations.engine import RecommendationEngine

def test_high_risk_customer_receives_discount_recommendation():
    actions = RecommendationEngine().recommend(
        {"contract": "Month-to-month", "monthly_charges": 95, "tenure": 3, "tech_support": "No"},
        {"churn_probability": 0.82},
    )
    assert actions[0]["action_type"] == "discount"
    assert any(a["action_type"] == "plan_change" for a in actions)

