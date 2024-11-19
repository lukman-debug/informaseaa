# myapp/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'homepage.html')
def dashboard(request):
    return render(request, 'dashboard.html')
