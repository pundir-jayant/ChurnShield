# ChurnShield

### Explainable AI-Based Customer Churn Prevention and Retention System

An Explainable AI-powered customer churn prediction and retention platform that leverages Machine Learning, XGBoost, SHAP explainability, analytics dashboards, and personalized retention recommendations to help businesses identify, understand, and retain at-risk customers.

---

## Features

* Customer Churn Prediction using Machine Learning
* Explainable AI (XAI) with SHAP
* Customer Risk Segmentation
* Personalized Retention Recommendations
* Interactive Analytics Dashboard
* Dataset Upload & Management
* Authentication & Authorization
* REST APIs with JWT Authentication
* PDF Report Generation
* Dockerized Deployment Support

---

## Tech Stack

### Backend

* Django 5
* Django REST Framework
* Simple JWT

### Machine Learning

* Scikit-Learn
* XGBoost
* SHAP
* Pandas
* NumPy

### Frontend

* HTML5
* Tailwind CSS
* Chart.js
* Lucide Icons

### Database

* SQLite (Development)
* PostgreSQL (Production Ready)

### Deployment

* Docker
* Gunicorn
* Nginx

---

## Project Architecture

```text
backend/
│
├── accounts/
├── analytics/
├── customers/
├── prediction/
├── recommendations/
├── reports/
├── ml/
│
├── config/

templates/
static/
datasets/
docs/
deployment/
research/
```

---

## Installation

```bash
git clone https://github.com/pundir-jayant/ChurnShield.git

cd ChurnShield

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

---

## Model Training

```bash
python manage.py train_churn_model --dataset datasets/sample_churn.csv
```

---

## API Endpoints

| Method | Endpoint                      |
| ------ | ----------------------------- |
| POST   | /api/auth/register/           |
| POST   | /api/auth/token/              |
| GET    | /api/dashboard/summary/       |
| POST   | /api/predictions/predict/     |
| POST   | /api/datasets/upload/         |
| GET    | /api/analytics/model-metrics/ |
| POST   | /api/reports/prediction/<id>/ |

---

## Research Deliverables

* Final Year Project Report
* IEEE Research Paper Draft
* Viva Preparation Questions
* Deployment Documentation

---

## Docker Deployment

```bash
docker compose up --build
```

Application runs at:

```text
http://localhost:8000
```

---

## Future Enhancements

* Deep Learning-Based Churn Prediction
* Real-Time Prediction APIs
* Customer Lifetime Value Prediction
* Multi-Tenant SaaS Support
* Automated Retention Campaigns
* AI-Powered Customer Insights

---

## Author

**Jayant Raj Pundir**

B.Tech CSE (Artificial Intelligence & Machine Learning)

Final Year Major Project

---

## License

This project is developed for educational and research purposes.
