from django.urls import path
from . import views

urlpatterns = [
    path('', views.kapal_list, name='kapal_list'),
    path('create/', views.kapal_create, name='kapal_create'),
    path('<int:pk>/', views.kapal_detail, name='kapal_detail'),
    path('<int:pk>/edit/', views.kapal_edit, name='kapal_edit'),
    path('<int:pk>/delete/', views.kapal_delete, name='kapal_delete'),
    path('api/list/', views.kapal_api_list, name='kapal_api_list'),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('export-excel/', views.export_excel, name='kapal_export_excel'),
]