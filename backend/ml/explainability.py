import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd

try:
    import shap
except Exception:  # pragma: no cover - SHAP can be heavy in minimal deployments.
    shap = None

class ExplainabilityService:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def feature_attribution(self, row):
        if shap is None or self.pipeline is None:
            return {"method": "fallback", "top_features": []}
        frame = pd.DataFrame([row])
        transformed = self.pipeline.named_steps["preprocessor"].transform(frame)
        model = self.pipeline.named_steps["model"]
        explainer = shap.Explainer(model)
        values = explainer(transformed)
        impacts = values.values[0].tolist()
        names = [f"feature_{i}" for i in range(len(impacts))]
        ranked = sorted(zip(names, impacts), key=lambda x: abs(x[1]), reverse=True)[:10]
        return {"method": "SHAP", "top_features": [{"feature": n, "impact": float(v)} for n, v in ranked]}

    def summary_plot_base64(self, sample_frame):
        if shap is None or self.pipeline is None:
            return ""
        transformed = self.pipeline.named_steps["preprocessor"].transform(sample_frame)
        model = self.pipeline.named_steps["model"]
        values = shap.Explainer(model)(transformed)
        shap.summary_plot(values, transformed, show=False)
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png", dpi=160)
        plt.close()
        return base64.b64encode(buf.getvalue()).decode("utf-8")

