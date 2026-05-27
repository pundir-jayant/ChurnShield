from django.conf import settings
from django.db import models
from backend.customers.models import Customer

class UploadedDataset(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="datasets/")
    original_name = models.CharField(max_length=255)
    row_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=30, default="uploaded")
    validation_errors = models.JSONField(default=list, blank=True)
    preview = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Prediction(models.Model):
    RISK_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="predictions", null=True, blank=True)
    dataset = models.ForeignKey(UploadedDataset, on_delete=models.SET_NULL, null=True, blank=True)
    input_payload = models.JSONField(default=dict)
    churn_probability = models.FloatField()
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES)
    predicted_label = models.BooleanField(default=False)
    model_name = models.CharField(max_length=120)
    explanation = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

