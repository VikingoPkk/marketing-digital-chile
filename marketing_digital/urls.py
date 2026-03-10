from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from courses import views as courses_views
from agency import views as agency_views
from courses.views import CursoListAPI, LessonListAPI, ToggleCompleteAPI
# Importamos las vistas de SimpleJWT para el Login sincronizado con la App
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # --- ADMINISTRACIÓN Y CUENTAS WEB ---
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # --- RUTAS DEL BLOG (MD CHILE) ---
    path('blog/', courses_views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', courses_views.blog_detail, name='blog_detail'),
    path('comment/add/<int:post_id>/', agency_views.add_comment, name='add_comment'),

    # --- RUTAS GENERALES DE LA ACADEMIA Y LEGAL ---
    path('', include('courses.urls')),
    path('privacidad/', agency_views.privacidad, name='privacidad'),
    path('terminos/', agency_views.terminos, name='terminos'),
    path('users/', include('users.urls')),

    # --- ENDPOINTS DE AUTENTICACIÓN (LOGIN ÚNICO WEB/APP) ---
    # Esta es la URL que el AuthService de Flutter usará para validar usuarios
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- API DE CONTENIDO PARA LA APP (FLUTTER) ---
    path('api/cursos/', CursoListAPI.as_view(), name='api-cursos'),
    path('api/cursos/<int:course_id>/lecciones/', LessonListAPI.as_view(), name='api-lecciones'),
    path('api/lecciones/<int:lesson_id>/completar/', ToggleCompleteAPI.as_view(), name='api-leccion-completar'),
    
]

# Servir archivos multimedia (Para ver las miniaturas de los cursos en la App)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)