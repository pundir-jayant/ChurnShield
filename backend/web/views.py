from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def datasets(request):
    return render(request, "datasets.html")

@login_required
def predictions(request):
    return render(request, "predict.html")

@login_required
def analytics(request):
    return render(request, "analytics.html")

