import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from pathlib import Path

from backend.customers.models import Customer
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

@pytest.mark.django_db
def test_dataset_upload_preview_and_batch_score(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"
    settings.ML_ARTIFACT_DIR = tmp_path / "models"
    user = User.objects.create_user(username="dataset_user", password="StrongPass123")
    client.force_login(user)
    content = Path("datasets/sample_churn.csv").read_bytes()
    upload = SimpleUploadedFile("sample_churn.csv", content, content_type="text/csv")

    create_response = client.post("/api/datasets/", {"file": upload})
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["status"] == "validated"
    assert created["preview"]

    batch_response = client.post(f"/api/datasets/{created['id']}/batch_predict/")
    assert batch_response.status_code == 200
    batch = batch_response.json()
    assert batch["count"] == 20
    assert sum(batch["risk_distribution"].values()) == 20
    assert Customer.objects.count() == 20
    assert Prediction.objects.filter(dataset_id=created["id"]).count() == 20

@pytest.mark.django_db
def test_dataset_upload_returns_preview_even_when_validation_fails(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"
    user = User.objects.create_user(username="bad_dataset_user", password="StrongPass123")
    client.force_login(user)
    upload = SimpleUploadedFile("bad.csv", b"customerID,tenure\nC-1,4\n", content_type="text/csv")

    response = client.post("/api/datasets/", {"file": upload})
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "failed"
    assert data["preview"]
    assert "Missing required columns" in data["validation_errors"][0]
