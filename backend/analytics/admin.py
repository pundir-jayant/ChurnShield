from django.contrib import admin
from .models import AnalyticsLog, ModelMetric

admin.site.register(AnalyticsLog)
admin.site.register(ModelMetric)

