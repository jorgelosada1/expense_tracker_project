# config/urls.py

from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    
    # Conectamos las URLs de nuestra aplicación 'core' a la raíz del sitio
    path('', include('core.urls')), 
]