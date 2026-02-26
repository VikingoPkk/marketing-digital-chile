from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importamos TODAS las funciones desde courses/views.py
from courses.views import (
    home, dashboard, course_detail, 
    toggle_lesson_completion, enroll_trial, checkout, take_quiz,
    edit_profile, check_certificate, generate_diploma_pdf
)

# Importamos las funciones de la Agencia
from agency.views import services_list, service_detail, contact_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # --- RUTAS DE LA ACADEMIA ---
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('checkout/<int:course_id>/', checkout, name='checkout'),
    path('enroll-trial/<int:course_id>/', enroll_trial, name='enroll_trial'),
    path('toggle-lesson/<int:lesson_id>/', toggle_lesson_completion, name='toggle_lesson'),
    path('quiz/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    
    # --- RUTAS DE DIPLOMAS ---
    path('verificar-certificado/<int:course_id>/', check_certificate, name='check_certificate'),
    path('descargar-diploma/<int:certificate_id>/', generate_diploma_pdf, name='generate_diploma_pdf'),

    # --- RUTAS DE LA AGENCIA ---
    path('servicios/', services_list, name='services_list'),
    path('servicios/<slug:slug>/', service_detail, name='service_detail'),
    path('contacto/', contact_view, name='contact_view'),
]

# Servir archivos multimedia (imágenes de cursos y agencia) en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)