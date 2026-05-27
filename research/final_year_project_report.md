# Explainable AI-Based Customer Churn Prevention and Retention System

## Abstract
This project presents an explainable AI platform for predicting customer churn, identifying the drivers behind churn risk, and recommending retention actions. The system combines Django, REST APIs, machine learning pipelines, model comparison, explainability, dashboards, CSV batch scoring, and PDF reporting.

## Existing System
Traditional churn systems often provide static reports or black-box predictions. They lack individual explanations, recommendation logic, batch workflows, and production-grade web interfaces.

## Proposed System
The proposed system predicts churn probability, classifies customers into risk categories, explains feature-level drivers, and recommends retention strategies such as discounts, loyalty rewards, support outreach, and plan right-sizing.

## Methodology
Data is ingested from CSV or manual forms, cleaned through imputers and encoders, transformed using scaling and one-hot encoding, and split into train/test sets. Multiple classifiers are trained and compared. The best model is persisted and served through Django APIs.

## Algorithms Used
Logistic Regression provides interpretable linear baseline performance. Decision Tree captures simple nonlinear rules. Random Forest reduces variance through ensemble learning. XGBoost provides high-performance gradient boosting for tabular churn data.

## Evaluation Metrics
Accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix are used. Recall is important because missing likely churners has business cost, while precision controls wasted retention spend.

## Explainable AI
The platform exposes SHAP-compatible feature attribution. In production, the explanation module can be extended with `shap.TreeExplainer` or `shap.Explainer` over the saved pipeline to generate summary, waterfall, and force visualizations.

## Results and Discussion
The model comparison module records every training run. XGBoost and Random Forest are expected to perform strongly on structured churn datasets, while Logistic Regression provides a stable baseline.

## Conclusion
The system demonstrates a complete AI SaaS workflow from data upload to prediction, explanation, recommendation, reporting, and deployment. It is suitable for academic presentation, portfolio demonstration, and extension into a production retention platform.

## Future Scope
Future improvements include live CRM integration, email automation, real-time event streaming, advanced segmentation, LLM-assisted retention scripts, and scheduled model retraining with drift monitoring.

## References
- Lundberg, S. M., and Lee, S. I. "A Unified Approach to Interpreting Model Predictions."
- Chen, T., and Guestrin, C. "XGBoost: A Scalable Tree Boosting System."
- Pedregosa et al. "Scikit-learn: Machine Learning in Python."
- Django Software Foundation documentation.
- Telecom customer churn benchmark literature.

