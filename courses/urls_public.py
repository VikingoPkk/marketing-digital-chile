from django.urls import path
from . import views_public

urlpatterns = [
    path('academia/', views_public.academia_publica, name='academia_publica'),
    path('academia/<slug:slug>/', views_public.curso_detalle_publico, name='public_course_detail'),
]