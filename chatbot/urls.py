from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatgpt, name='chatgpt'),  # Route untuk HTML
    path('api/', views.chatgpt_api_view, name='chatgpt_api'),  # Route untuk API
]
