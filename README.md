
# ChurnShield — Explainable AI-Based Customer Churn Prevention and Retention System

Industry-style project for churn prediction, explainability, retention recommendations, analytics, and reporting.

## Stack
- Django 5, Django REST Framework, Simple JWT
- PostgreSQL-ready database config with SQLite fallback
- Scikit-learn, XGBoost, SHAP, Pandas, NumPy
- Tailwind CSS CDN, Chart.js, Lucide icons
- Docker, Gunicorn, Nginx-ready deployment

## Quick Start
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py train_churn_model --dataset datasets/sample_churn.csv
python manage.py runserver
```

Open http://127.0.0.1:8000

## API Highlights
- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `GET /api/dashboard/summary/`
- `POST /api/predictions/predict/`
- `POST /api/datasets/upload/`
- `GET /api/analytics/model-metrics/`
- `POST /api/reports/prediction/<id>/`

## Project Structure
```text
backend/
  config/                 Django settings and URLs
  accounts/               User registration and auth APIs
  customers/              Customer entity and admin
  prediction/             Prediction APIs and CSV upload
  analytics/              Dashboard APIs
  recommendations/        Retention recommendation engine
  reports/                PDF/report generation
  ml/                     Training, preprocessing, explainability
templates/                SaaS dashboard UI
static/                   CSS/JS assets
datasets/                 Sample churn dataset
docs/                     API, deployment, testing docs
deployment/               Docker/Nginx/Gunicorn assets
```

## Docker
```powershell
docker compose up --build
```

The app listens on http://localhost:8000.
