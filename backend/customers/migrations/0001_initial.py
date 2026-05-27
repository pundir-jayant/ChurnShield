from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="Customer", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("customer_id", models.CharField(max_length=80, unique=True)),
        ("name", models.CharField(blank=True, max_length=160)),
        ("email", models.EmailField(blank=True, max_length=254)),
        ("gender", models.CharField(blank=True, max_length=20)),
        ("senior_citizen", models.BooleanField(default=False)),
        ("partner", models.BooleanField(default=False)),
        ("dependents", models.BooleanField(default=False)),
        ("tenure", models.PositiveIntegerField(default=0)),
        ("contract", models.CharField(blank=True, max_length=80)),
        ("internet_service", models.CharField(blank=True, max_length=80)),
        ("monthly_charges", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
        ("total_charges", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
        ("created_at", models.DateTimeField(auto_now_add=True)),
        ("updated_at", models.DateTimeField(auto_now=True)),
    ], options={"ordering": ["-created_at"]})]

