from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from courses.views import (
    home, dashboard, course_detail, 
    toggle_lesson_completion, enroll_trial, checkout, take_quiz,
    edit_profile  # Asegúrate de que esta importación esté presente
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('checkout/<int:course_id>/', checkout, name='checkout'),
    path('enroll-trial/<int:course_id>/', enroll_trial, name='enroll_trial'),
    path('toggle-lesson/<int:lesson_id>/', toggle_lesson_completion, name='toggle_lesson'),
    path('quiz/<int:quiz_id>/', take_quiz, name='take_quiz'),
    
    # NUEVA RUTA PARA EL PERFIL
    path('profile/edit/', edit_profile, name='edit_profile'),
]

# Esto permite que Django sirva las imágenes de perfil y de los cursos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)