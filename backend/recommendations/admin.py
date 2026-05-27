from django.contrib import admin
from .models import Recommendation

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("title", "action_type", "priority", "estimated_impact", "created_at")
    list_filter = ("priority", "action_type")

