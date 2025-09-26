from django.urls import path
from . import views

app_name = 'kapal'

urlpatterns = [
    # Main kapal management page
    path('', views.kapal_list, name='list'),
    
    # CRUD operations
    path('add/', views.kapal_add, name='add'),
    path('<int:pk>/', views.kapal_detail, name='detail'),
    path('<int:pk>/edit/', views.kapal_edit, name='edit'),
    path('<int:pk>/delete/', views.kapal_delete, name='delete'),
    
    # Document management
    path('<int:pk>/upload-document/', views.upload_document, name='upload_document'),
    path('<int:pk>/delete-document/', views.delete_document, name='delete_document'),
    
    # API endpoints
    path('api/camera-upload/', views.camera_upload, name='camera_upload'),
    path('api/validate-file/', views.validate_file, name='validate_file'),
]