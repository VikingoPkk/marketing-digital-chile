from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # Priorizamos la ruta de servicios para que no se pierda en 'courses'
    # Esta línea debe ser la única que maneje las páginas de la academia
    path('', include('courses.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)