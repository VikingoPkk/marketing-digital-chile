from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Conexión con la academia
    path('', include('courses.urls')), 
    
    # Ruta temporal para evitar el error de 'contact_view'
    path('contacto-temporal/', lambda r: HttpResponse("Pronto..."), name='contact_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)