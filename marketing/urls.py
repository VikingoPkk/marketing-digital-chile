from django.urls import path
from . import views, admin_views

urlpatterns = [
    # El action del formulario apunta a este 'name'
    path('lanzar/', views.lanzar_campaña_view, name='lanzar_campaña'),
    
    # Rutas de tracking (Pixel y Clicks)
    path('open/<int:tracking_id>/pixel.gif', views.track_apertura, name='mail_open'),
    path('click/<int:tracking_id>/', views.track_click, name='mail_click'),
    
    # Ruta de estadísticas (Dashboard de Marketing)
    path('stats/', admin_views.dashboard_marketing, name='marketing_stats'),
]