from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("customer_id", "name", "contract", "tenure", "monthly_charges", "created_at")
    search_fields = ("customer_id", "name", "email")
    list_filter = ("contract", "internet_service", "senior_citizen")

