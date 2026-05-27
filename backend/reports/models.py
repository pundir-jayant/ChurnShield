from django.conf import settings
from django.db import models

class GeneratedReport(models.Model):
    REPORT_TYPES = [("prediction", "Prediction"), ("analytics", "Analytics"), ("research", "Research")]
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    report_type = models.CharField(max_length=40, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="reports/")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

