from django.contrib import admin
from .models import Prediction, UploadedDataset

@admin.register(UploadedDataset)
class UploadedDatasetAdmin(admin.ModelAdmin):
    list_display = ("original_name", "row_count", "status", "uploaded_by", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("original_name",)

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("id", "risk_level", "churn_probability", "model_name", "created_at")
    list_filter = ("risk_level", "model_name", "created_at")

