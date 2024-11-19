from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='tanyapeta'),
    path('spl/', views.get_spl_data, name='data'),
    path('klorofil/', views.get_klorofil_data, name='klorofil'),
    path('fishing/', views.fishing_zone, name='fishing'),
    path('mangrove/', views.get_mangrove_data, name='mangrove'),
    path('lamun/', views.get_lamun_data, name='lamun'),
    path('karang/', views.get_karang_data, name='karang'),
]
