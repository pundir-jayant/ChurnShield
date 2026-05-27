from django.db import models
from backend.prediction.models import Prediction

class Recommendation(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name="recommendations")
    title = models.CharField(max_length=160)
    action_type = models.CharField(max_length=80)
    priority = models.CharField(max_length=20, default="medium")
    rationale = models.TextField()
    estimated_impact = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

