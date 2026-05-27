import pandas as pd

class RecommendationEngine:
    def _value(self, customer, *keys, default=None):
        for key in keys:
            value = customer.get(key)
            if value not in (None, "") and not pd.isna(value):
                return value
        return default

    def recommend(self, customer, prediction):
        probability = prediction["churn_probability"]
        monthly = float(self._value(customer, "monthly_charges", "MonthlyCharges", default=0))
        contract = self._value(customer, "contract", "Contract", default="")
        tenure = int(float(self._value(customer, "tenure", default=0)))
        actions = []
        if probability >= 0.7:
            actions.append({"title": "Retention save offer", "action_type": "discount", "priority": "high", "rationale": "High churn probability indicates immediate incentive is justified.", "estimated_impact": 0.18})
        if contract == "Month-to-month":
            actions.append({"title": "Annual plan migration", "action_type": "plan_change", "priority": "high", "rationale": "Month-to-month customers are historically more volatile.", "estimated_impact": 0.14})
        if monthly > 70:
            actions.append({"title": "Plan right-sizing consultation", "action_type": "plan_downgrade", "priority": "medium", "rationale": "High monthly charges can create price sensitivity.", "estimated_impact": 0.11})
        if tenure < 6:
            actions.append({"title": "Onboarding success call", "action_type": "support", "priority": "medium", "rationale": "New customers need early value reinforcement.", "estimated_impact": 0.09})
        actions.append({"title": "Personalized loyalty reward", "action_type": "loyalty", "priority": "low", "rationale": "Loyalty benefits increase perceived switching cost.", "estimated_impact": 0.07})
        return actions[:4]
