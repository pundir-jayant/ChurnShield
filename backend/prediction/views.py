import pandas as pd
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.customers.models import Customer
from backend.ml.inference import ChurnPredictor
from backend.ml.preprocessing import CATEGORICAL_FEATURES, NUMERIC_FEATURES, normalize_columns
from backend.recommendations.engine import RecommendationEngine
from backend.recommendations.models import Recommendation
from .models import Prediction, UploadedDataset
from .serializers import ManualPredictionSerializer, PredictionSerializer, UploadedDatasetSerializer

def _row_value(row, *keys, default=""):
    for key in keys:
        value = row.get(key)
        if value is not None and not pd.isna(value):
            return value
    return default

def _row_bool(row, *keys):
    value = str(_row_value(row, *keys, default="No")).strip().lower()
    return value in {"1", "true", "yes", "y"}

def _row_float(row, *keys):
    value = _row_value(row, *keys, default=0)
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0

def _row_int(row, *keys):
    return int(_row_float(row, *keys))

class DatasetUploadViewSet(viewsets.ModelViewSet):
    queryset = UploadedDataset.objects.all()
    serializer_class = UploadedDatasetSerializer

    def perform_create(self, serializer):
        dataset = serializer.save(uploaded_by=self.request.user, original_name=self.request.FILES["file"].name)
        try:
            df = pd.read_csv(dataset.file.path)
            normalized_df = normalize_columns(df)
            required = set(NUMERIC_FEATURES + CATEGORICAL_FEATURES)
            missing = sorted(required - set(normalized_df.columns))
            if missing:
                dataset.status = "failed"
                dataset.validation_errors = [f"Missing required columns: {', '.join(missing)}"]
                dataset.save(update_fields=["status", "validation_errors"])
                return
            dataset.row_count = len(df)
            dataset.preview = df.head(8).fillna("").to_dict("records")
            dataset.status = "validated"
            dataset.save(update_fields=["row_count", "preview", "status"])
        except Exception as exc:
            dataset.status = "failed"
            dataset.validation_errors = [str(exc)]
            dataset.save(update_fields=["status", "validation_errors"])

    @action(detail=True, methods=["post"])
    def batch_predict(self, request, pk=None):
        dataset = self.get_object()
        if dataset.status == "failed":
            return Response({"detail": "Dataset validation failed.", "errors": dataset.validation_errors}, status=status.HTTP_400_BAD_REQUEST)
        df = pd.read_csv(dataset.file.path)
        predictor = ChurnPredictor()
        results = []
        for index, row in enumerate(df.to_dict("records"), start=1):
            customer_id = str(_row_value(row, "customerID", "customer_id", default=f"dataset-{dataset.id}-{index}"))
            customer, _ = Customer.objects.update_or_create(
                customer_id=customer_id,
                defaults={
                    "name": str(_row_value(row, "name", "Name", default="")),
                    "email": str(_row_value(row, "email", "Email", default="")),
                    "gender": str(_row_value(row, "gender", default="")),
                    "senior_citizen": _row_bool(row, "SeniorCitizen", "senior_citizen"),
                    "partner": _row_bool(row, "Partner", "partner"),
                    "dependents": _row_bool(row, "Dependents", "dependents"),
                    "tenure": _row_int(row, "tenure"),
                    "contract": str(_row_value(row, "Contract", "contract", default="")),
                    "internet_service": str(_row_value(row, "InternetService", "internet_service", default="")),
                    "monthly_charges": _row_float(row, "MonthlyCharges", "monthly_charges"),
                    "total_charges": _row_float(row, "TotalCharges", "total_charges"),
                },
            )
            result = predictor.predict(row)
            pred = Prediction.objects.create(
                customer=customer, dataset=dataset, input_payload=row, churn_probability=result["churn_probability"],
                risk_level=result["risk_level"], predicted_label=result["predicted_label"],
                model_name=result["model_name"], explanation=result["explanation"], created_by=request.user,
            )
            results.append(PredictionSerializer(pred).data)
        dataset.status = "predicted"
        dataset.save(update_fields=["status"])
        return Response({"count": len(results), "results": results})

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.select_related("customer", "dataset").all()
    serializer_class = PredictionSerializer

    @action(detail=False, methods=["post"])
    def predict(self, request):
        serializer = ManualPredictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = ChurnPredictor().predict(serializer.validated_data)
        recommendation_payload = RecommendationEngine().recommend(serializer.validated_data, result)
        pred = Prediction.objects.create(
            input_payload=serializer.validated_data,
            churn_probability=result["churn_probability"],
            risk_level=result["risk_level"],
            predicted_label=result["predicted_label"],
            model_name=result["model_name"],
            explanation=result["explanation"],
            created_by=request.user,
        )
        Recommendation.objects.bulk_create([Recommendation(prediction=pred, **item) for item in recommendation_payload])
        return Response({"prediction": PredictionSerializer(pred).data, "recommendations": recommendation_payload}, status=status.HTTP_201_CREATED)
