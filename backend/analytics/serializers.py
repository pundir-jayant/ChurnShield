from rest_framework import serializers
from .models import ModelMetric

class ModelMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelMetric
        fields = "__all__"

