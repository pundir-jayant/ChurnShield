# Viva Questions With Answers

1. What is customer churn?
Customer churn is the loss of customers over a period. In this project, churn is modeled as a binary classification problem.

2. Why use explainable AI?
Prediction alone is not actionable. SHAP-style explanations identify the features influencing each churn decision.

3. Which models are compared?
Logistic Regression, Decision Tree, Random Forest, and XGBoost are trained and compared using accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix.

4. Why ROC-AUC?
ROC-AUC evaluates ranking quality across thresholds and is useful when churn classes are imbalanced.

5. How are retention recommendations generated?
A rule-based scoring engine maps risk drivers such as high charges, short tenure, missing support, and month-to-month contract to targeted actions.

6. How is the best model selected?
The training pipeline selects the model with the highest ROC-AUC and saves it as `ml_models/best_churn_model.joblib`.

7. What is the role of Django REST Framework?
DRF exposes prediction, analytics, dataset, recommendation, and reporting APIs with serializers, viewsets, validation, and pagination.

8. How is the project deployment-ready?
It includes environment-based settings, Gunicorn, static file handling, Docker Compose, and production deployment documentation.

