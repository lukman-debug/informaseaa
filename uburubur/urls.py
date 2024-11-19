from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='uburubur'),
    path('predict/', views.predict, name='predict'),
]
