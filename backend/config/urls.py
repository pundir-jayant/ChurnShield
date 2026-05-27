from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from backend.accounts.views import RegisterAPIView, register_page
from backend.analytics.views import DashboardSummaryAPIView, ModelMetricViewSet
from backend.prediction.views import DatasetUploadViewSet, PredictionViewSet
from backend.recommendations.views import RecommendationViewSet
from backend.reports.views import ReportViewSet
from backend.web.views import dashboard, datasets, predictions, analytics

router = DefaultRouter()
router.register("datasets", DatasetUploadViewSet, basename="datasets")
router.register("predictions", PredictionViewSet, basename="predictions")
router.register("recommendations", RecommendationViewSet, basename="recommendations")
router.register("reports", ReportViewSet, basename="reports")
router.register("analytics/model-metrics", ModelMetricViewSet, basename="model-metrics")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("login/", LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("register/", register_page, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("datasets/", datasets, name="datasets"),
    path("predict/", predictions, name="predict"),
    path("analytics/", analytics, name="analytics"),
    path("api/auth/register/", RegisterAPIView.as_view(), name="api-register"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/dashboard/summary/", DashboardSummaryAPIView.as_view(), name="dashboard-summary"),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
