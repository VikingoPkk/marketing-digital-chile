from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from courses import views  # Importamos las vistas para acceder al blog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # RUTAS DEL BLOG
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Priorizamos la ruta de servicios para que no se pierda en 'courses'
    path('', include('courses.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)