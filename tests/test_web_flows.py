import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from backend.prediction.models import Prediction
from backend.recommendations.models import Recommendation

@pytest.mark.django_db
def test_dashboard_redirects_to_project_login(client):
    response = client.get("/", follow=False)
    assert response.status_code == 302
    assert response["Location"].startswith("/login/")

@pytest.mark.django_db
def test_register_page_creates_user_and_logs_in(client):
    response = client.post(reverse("register"), {
        "username": "analyst_review",
        "email": "analyst@example.com",
        "first_name": "AI",
        "last_name": "Analyst",
        "role": "analyst",
        "password1": "StrongPass123",
        "password2": "StrongPass123",
    }, follow=True)
    assert response.status_code == 200
    assert User.objects.filter(username="analyst_review").exists()
    assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_manual_prediction_persists_recommendations(client, settings, tmp_path):
    settings.ML_ARTIFACT_DIR = tmp_path
    user = User.objects.create_user(username="api_user", password="StrongPass123")
    client.force_login(user)
    payload = {
        "gender": "Female",
        "senior_citizen": False,
        "partner": "Yes",
        "dependents": "No",
        "tenure": 3,
        "phone_service": "Yes",
        "multiple_lines": "No",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "tech_support": "No",
        "contract": "Month-to-month",
        "paperless_billing": "Yes",
        "payment_method": "Electronic check",
        "monthly_charges": 91.0,
        "total_charges": 273.0,
    }
    response = client.post("/api/predictions/predict/", payload, content_type="application/json")
    assert response.status_code == 201
    assert Prediction.objects.count() == 1
    assert Recommendation.objects.filter(prediction=Prediction.objects.first()).exists()

