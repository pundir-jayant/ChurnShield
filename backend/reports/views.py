from pathlib import Path
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.prediction.models import Prediction
from .models import GeneratedReport
from .serializers import GeneratedReportSerializer

class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GeneratedReport.objects.all()
    serializer_class = GeneratedReportSerializer

    @action(detail=False, methods=["post"], url_path="prediction/(?P<prediction_id>[^/.]+)")
    def prediction_report(self, request, prediction_id=None):
        prediction = Prediction.objects.get(pk=prediction_id)
        out_dir = Path(settings.MEDIA_ROOT) / "reports"
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = f"prediction_report_{prediction.id}.pdf"
        path = out_dir / filename
        pdf = canvas.Canvas(str(path), pagesize=A4)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(72, 800, "Customer Churn Prediction Report")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(72, 765, f"Probability: {prediction.churn_probability:.2%}")
        pdf.drawString(72, 745, f"Risk level: {prediction.risk_level.title()}")
        pdf.drawString(72, 725, f"Model: {prediction.model_name}")
        pdf.drawString(72, 705, "Top explanation factors:")
        y = 685
        for item in prediction.explanation.get("top_features", [])[:8]:
            pdf.drawString(90, y, f"- {item['feature']}: {item['impact']:.4f}")
            y -= 18
        pdf.save()
        report = GeneratedReport.objects.create(
            generated_by=request.user, report_type="prediction", title="Prediction Report",
            file=f"reports/{filename}", metadata={"prediction_id": prediction.id},
        )
        return Response(GeneratedReportSerializer(report).data)

