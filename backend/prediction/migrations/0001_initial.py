import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("customers", "0001_initial")]
    operations = [
        migrations.CreateModel(name="UploadedDataset", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("file", models.FileField(upload_to="datasets/")),
            ("original_name", models.CharField(max_length=255)),
            ("row_count", models.PositiveIntegerField(default=0)),
            ("status", models.CharField(default="uploaded", max_length=30)),
            ("validation_errors", models.JSONField(blank=True, default=list)),
            ("preview", models.JSONField(blank=True, default=list)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("uploaded_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="Prediction", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("input_payload", models.JSONField(default=dict)),
            ("churn_probability", models.FloatField()),
            ("risk_level", models.CharField(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], max_length=20)),
            ("predicted_label", models.BooleanField(default=False)),
            ("model_name", models.CharField(max_length=120)),
            ("explanation", models.JSONField(blank=True, default=dict)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("created_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ("customer", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="predictions", to="customers.customer")),
            ("dataset", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="prediction.uploadeddataset")),
        ], options={"ordering": ["-created_at"]}),
    ]

