from django.db import models

class Customer(models.Model):
    customer_id = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=160, blank=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=20, blank=True)
    senior_citizen = models.BooleanField(default=False)
    partner = models.BooleanField(default=False)
    dependents = models.BooleanField(default=False)
    tenure = models.PositiveIntegerField(default=0)
    contract = models.CharField(max_length=80, blank=True)
    internet_service = models.CharField(max_length=80, blank=True)
    monthly_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_id} - {self.name or 'Customer'}"

