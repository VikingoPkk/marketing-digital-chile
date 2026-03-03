from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from courses import views as courses_views
from agency import views as agency_views
from courses.views import CursoListAPI, LessonListAPI, ToggleCompleteAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # --- RUTAS DEL BLOG ---
    path('blog/', courses_views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', courses_views.blog_detail, name='blog_detail'),
    path('comment/add/<int:post_id>/', agency_views.add_comment, name='add_comment'),

    # Rutas generales de la academia
    path('', include('courses.urls')),
    path('privacidad/', agency_views.privacidad, name='privacidad'),
    path('terminos/', agency_views.terminos, name='terminos'),

    # --- ENDPOINT PARA LA APP DE IRON MAN (FLUTTER) ---
    path('api/cursos/', CursoListAPI.as_view(), name='api-cursos'),
    path('api/cursos/<int:course_id>/lecciones/', LessonListAPI.as_view(), name='api-lecciones'),
    path('api/lecciones/<int:lesson_id>/completar/', ToggleCompleteAPI.as_view(), name='api-leccion-completar'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)