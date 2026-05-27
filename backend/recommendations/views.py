from rest_framework import viewsets
from .models import Recommendation
from .serializers import RecommendationSerializer

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.select_related("prediction").all()
    serializer_class = RecommendationSerializer

