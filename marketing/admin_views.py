from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import CampañaPro, TrackingCorreo

@staff_member_required
def dashboard_marketing(request):
    # Traemos todas las campañas de la historia, la más reciente primero
    campañas = CampañaPro.objects.all().order_by('-fecha_creacion')
    
    stats_list = []
    for c in campañas:
        tasa_apertura = (c.aperturas_unicas / c.total_enviados * 100) if c.total_enviados > 0 else 0
        
        # Obtenemos el detalle de qué alumnos interactuaron con ESTA campaña
        detalle_interaccion = TrackingCorreo.objects.filter(campaña=c).select_related('usuario')

        stats_list.append({
            'campaña': c,
            'tasa_apertura': round(tasa_apertura, 1),
            'detalle': detalle_interaccion # Para la tabla de abajo
        })

    return render(request, 'marketing/dashboard.html', {'stats': stats_list})