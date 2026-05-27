import json
from pathlib import Path
import joblib
import pandas as pd
from django.conf import settings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from backend.analytics.models import ModelMetric
from .preprocessing import CATEGORICAL_FEATURES, NUMERIC_FEATURES, TARGET_COLUMN, build_preprocessor, clean_dataframe

MODELS = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=250, random_state=42, class_weight="balanced"),
    "XGBoost": XGBClassifier(n_estimators=250, max_depth=4, learning_rate=0.05, eval_metric="logloss", random_state=42),
}

def train_and_select(dataset_path):
    df = clean_dataframe(pd.read_csv(dataset_path))
    features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    X, y = df[features], df[TARGET_COLUMN]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    artifact_dir = Path(settings.ML_ARTIFACT_DIR)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    ModelMetric.objects.update(is_best=False)
    best = None
    best_metric_id = None
    metrics = []
    for name, estimator in MODELS.items():
        pipeline = Pipeline([("preprocessor", build_preprocessor()), ("model", estimator)])
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        probs = pipeline.predict_proba(X_test)[:, 1]
        record = {
            "model_name": name, "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall": recall_score(y_test, preds, zero_division=0),
            "f1_score": f1_score(y_test, preds, zero_division=0),
            "roc_auc": roc_auc_score(y_test, probs),
            "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
        }
        metrics.append(record)
        metric_obj = ModelMetric.objects.create(**record)
        if best is None or record["roc_auc"] > best["metrics"]["roc_auc"]:
            best = {"name": name, "pipeline": pipeline, "metrics": record}
            best_metric_id = metric_obj.id
    joblib.dump(best["pipeline"], artifact_dir / "best_churn_model.joblib")
    (artifact_dir / "metadata.json").write_text(json.dumps({"best_model": best["name"], "metrics": metrics}, indent=2))
    ModelMetric.objects.filter(id=best_metric_id).update(is_best=True)
    return {"best_model": best["name"], "metrics": metrics}
