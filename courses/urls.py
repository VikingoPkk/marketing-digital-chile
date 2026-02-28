from django.urls import path
from . import views

urlpatterns = [
    # --- NAVEGACIÓN PRINCIPAL ---
    path('', views.home, name='home'),
    path('contacto/', views.contact_page, name='contact_view'),
    
    # --- SISTEMA DE SERVICIOS Y LANDINGS (META SUITE) ---
    # Vitrina general de servicios
    path('servicios/', views.services_list, name='services_list'),
    # Landing Page individual por SLUG (Para tus campañas)
    path('servicios/<slug:slug>/', views.service_detail, name='service_detail'),
    
    # --- SISTEMA DE ACADEMIA (DASHBOARD Y CURSOS) ---
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll-trial/<int:course_id>/', views.enroll_trial, name='enroll_trial'),
    path('checkout/<int:course_id>/', views.checkout, name='checkout'),
    
    # --- LECCIONES Y PROGRESO ---
    # CORRECCIÓN AQUÍ: El nombre debe ser 'toggle_lesson_completion' para que el HTML lo encuentre
    path('toggle-lesson/<int:lesson_id>/', views.toggle_lesson_completion, name='toggle_lesson_completion'),
    
    # --- EXÁMENES Y PERFIL ---
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # --- DIPLOMAS Y CERTIFICADOS ---
    path('certificate/check/<int:course_id>/', views.check_certificate, name='check_certificate'),
    path('certificate/pdf/<int:certificate_id>/', views.generate_diploma_pdf, name='generate_diploma_pdf'),
]