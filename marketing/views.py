import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from .models import CampañaPro, TrackingCorreo
from .servicios_campaña import ejecutar_lanzamiento

User = get_user_model()

def track_apertura(request, tracking_id):
    """Pixel invisible para detectar aperturas"""
    tracking = get_object_or_404(TrackingCorreo, id=tracking_id)
    if not tracking.abierto:
        tracking.abierto = True
        tracking.fecha_apertura = datetime.datetime.now()
        tracking.save()
        campaña = tracking.campaña
        campaña.aperturas_unicas += 1
        campaña.save()
    pixel_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return HttpResponse(pixel_data, content_type="image/gif")

def track_click(request, tracking_id):
    """Registra el click y manda al alumno a la URL de destino"""
    tracking = get_object_or_404(TrackingCorreo, id=tracking_id)
    tracking.campaña.clicks_totales += 1
    tracking.campaña.save()
    # Aquí puedes poner la URL que quieras, por defecto al dashboard
    return HttpResponseRedirect("https://mdchile.cl/dashboard/")

def lanzar_campaña_view(request):
    """Esta es la función que procesa tu botón azul 'LANZAR CAMPAÑA'"""
    if request.method == 'POST':
        datos = {
            'asunto': request.POST.get('asunto'),
            'cuerpo': request.POST.get('cuerpo'), # El HTML del editor
            'url_destino': request.POST.get('url_destino'), # El link del botón naranja
        }
        
        # Seleccionamos a todos los alumnos activos
        alumnos = User.objects.filter(is_active=True)
        
        # Llamamos al motor de envío
        ejecutar_lanzamiento(datos, alumnos)
        
        # Cuando termina, te manda a ver las estadísticas
        return redirect('marketing_stats')
    
    # Si entras por error sin POST, te devuelve al dashboard
    return redirect('dashboard')