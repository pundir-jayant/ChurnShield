from rest_framework import serializers
from .models import Prediction, UploadedDataset

class UploadedDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDataset
        fields = "__all__"
        read_only_fields = ["uploaded_by", "row_count", "status", "validation_errors", "preview", "created_at"]

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]

class ManualPredictionSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=["Male", "Female"])
    senior_citizen = serializers.BooleanField()
    partner = serializers.ChoiceField(choices=["Yes", "No"])
    dependents = serializers.ChoiceField(choices=["Yes", "No"])
    tenure = serializers.IntegerField(min_value=0, max_value=100)
    phone_service = serializers.ChoiceField(choices=["Yes", "No"])
    multiple_lines = serializers.CharField()
    internet_service = serializers.ChoiceField(choices=["DSL", "Fiber optic", "No"])
    online_security = serializers.CharField()
    tech_support = serializers.CharField()
    contract = serializers.ChoiceField(choices=["Month-to-month", "One year", "Two year"])
    paperless_billing = serializers.ChoiceField(choices=["Yes", "No"])
    payment_method = serializers.CharField()
    monthly_charges = serializers.FloatField(min_value=0)
    total_charges = serializers.FloatField(min_value=0)

