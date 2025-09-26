"""
URL configuration for informasea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('chatbot/', include('chatbot.urls')),
    # path('uburubur/', include('uburubur.urls')),  # Temporarily disabled due to missing dependencies
    # path('prediksea/', include('prediksea.urls')),  # Temporarily disabled due to missing model files
    path('tanyapeta/', include('tanyapeta.urls')),
    path('ikan/', include('ikan_segar.urls')),
    path('deteksea/', include('deteksea.urls')),
    path('kapal/', include('kapal.urls')),  # New ship management app
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
