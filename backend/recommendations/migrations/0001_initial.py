import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [("prediction", "0001_initial")]
    operations = [migrations.CreateModel(name="Recommendation", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("title", models.CharField(max_length=160)),
        ("action_type", models.CharField(max_length=80)),
        ("priority", models.CharField(default="medium", max_length=20)),
        ("rationale", models.TextField()),
        ("estimated_impact", models.FloatField(default=0)),
        ("created_at", models.DateTimeField(auto_now_add=True)),
        ("prediction", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="recommendations", to="prediction.prediction")),
    ])]

