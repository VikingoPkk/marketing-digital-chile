from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from courses import views as courses_views  # Para las vistas del blog en courses
from agency import views as agency_views    # Para la nueva vista de comentarios en agency

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # --- RUTAS DEL BLOG (Aseguradas) ---
    path('blog/', courses_views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', courses_views.blog_detail, name='blog_detail'),
    
    # --- NUEVA RUTA PARA COMENTARIOS (Platzi Style) ---
    path('comment/add/<int:post_id>/', agency_views.add_comment, name='add_comment'),

    # Rutas generales de la academia
    path('', include('courses.urls')),
    
    path('privacidad/', agency_views.privacidad, name='privacidad'),
    path('terminos/', agency_views.terminos, name='terminos'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)