from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='wave'),
    path('predict/', views.predict_wave_height, name='predict_wave_height'),
]
