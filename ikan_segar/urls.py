from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='ikan'),
    path('predict/', views.predict, name='predict'),
]
