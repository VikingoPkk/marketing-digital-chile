from django.urls import path
from . import views

urlpatterns = [
    # 1. NAVEGACIÓN PRINCIPAL
    path('', views.home, name='home'),
    path('servicios/', views.services_list, name='services_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('contacto/', views.contact_page, name='contact_view'),

    # 2. SISTEMA DE CURSOS
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('checkout/<int:course_id>/', views.checkout, name='checkout'),
    path('enroll/<int:course_id>/', views.enroll_trial, name='enroll_trial'),
    path('lesson/toggle/<int:lesson_id>/', views.toggle_lesson_completion, name='toggle_lesson_completion'),

    # 3. EXÁMENES Y RESULTADOS
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/result/', views.take_quiz, name='quiz_result'), 

    # 4. SISTEMA DE DIPLOMAS MD CHILE
    path('verificar-certificado/<int:course_id>/', views.check_certificate, name='check_certificate'),
    path('descargar-diploma/<int:certificate_id>/', views.generate_diploma_pdf, name='generate_diploma_pdf'),
]