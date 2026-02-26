from django.contrib import admin
from django.urls import path, include
# Importamos todas las vistas necesarias desde courses.views
from courses.views import home, dashboard, course_detail, checkout, enroll_trial 

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Página de inicio (Landing Page)
    path('', home, name='home'),
    
    # Sistema de Cuentas (Login, Registro, Google, etc. manejado por allauth)
    path('accounts/', include('allauth.urls')),
    
    # Panel Principal del Alumno (Dashboard)
    path('dashboard/', dashboard, name='dashboard'), 

    # Detalle de cada curso (donde el alumno ve los videos)
    path('course/<int:course_id>/', course_detail, name='course_detail'),

    # Página de resumen de compra (Checkout)
    path('checkout/<int:course_id>/', checkout, name='checkout'),
    
    # Ruta que procesa la matrícula exitosa (Simulación de pago)
    path('enroll-success/<int:course_id>/', enroll_trial, name='enroll_trial'),
]