from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import CampañaPro, TrackingCorreo

@admin.register(CampañaPro)
class CampañaProAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'asunto', 'total_enviados', 'fecha_creacion', 'ver_analitica_btn')
    readonly_fields = ('titulo', 'asunto', 'contenido_html', 'total_enviados', 'aperturas_unicas', 'clicks_totales', 'enviada')

    def ver_analitica_btn(self, obj):
        url = reverse('marketing_stats')
        return format_html('<a class="btn btn-sm btn-info" href="{}"><i class="fas fa-chart-bar"></i> Ver Analítica</a>', url)
    ver_analitica_btn.short_description = "Acciones"

    def has_add_permission(self, request):
        return False

@admin.register(TrackingCorreo)
class TrackingCorreoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'campaña', 'abierto', 'fecha_apertura')