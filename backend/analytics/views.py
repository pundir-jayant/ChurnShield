from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.customers.models import Customer
from backend.prediction.models import Prediction, UploadedDataset
from .models import ModelMetric
from .serializers import ModelMetricSerializer

class DashboardSummaryAPIView(APIView):
    def get(self, request):
        total_predictions = Prediction.objects.count()
        high_risk = Prediction.objects.filter(risk_level="high").count()
        churn_rate = round((Prediction.objects.filter(predicted_label=True).count() / total_predictions) * 100, 2) if total_predictions else 0
        latest = list(Prediction.objects.values("risk_level", "churn_probability", "model_name", "created_at")[:10])
        return Response({
            "total_customers": Customer.objects.count(),
            "datasets": UploadedDataset.objects.count(),
            "total_predictions": total_predictions,
            "high_risk_customers": high_risk,
            "churn_rate": churn_rate,
            "active_customers": max(Customer.objects.count() - high_risk, 0),
            "latest_predictions": latest,
            "risk_distribution": {
                "low": Prediction.objects.filter(risk_level="low").count(),
                "medium": Prediction.objects.filter(risk_level="medium").count(),
                "high": high_risk,
            },
        })

class ModelMetricViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelMetric.objects.all()
    serializer_class = ModelMetricSerializer

