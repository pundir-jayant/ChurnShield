from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="AnalyticsLog", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("event_type", models.CharField(max_length=80)),
            ("payload", models.JSONField(default=dict)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.CreateModel(name="ModelMetric", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("model_name", models.CharField(max_length=120)),
            ("accuracy", models.FloatField()),
            ("precision", models.FloatField()),
            ("recall", models.FloatField()),
            ("f1_score", models.FloatField()),
            ("roc_auc", models.FloatField()),
            ("confusion_matrix", models.JSONField(default=list)),
            ("is_best", models.BooleanField(default=False)),
            ("trained_at", models.DateTimeField(auto_now_add=True)),
        ], options={"ordering": ["-trained_at"]}),
    ]

