from django.db import models
from django.conf import settings

class CampañaPro(models.Model):
    # Datos básicos
    titulo = models.CharField("Nombre Interno", max_length=200)
    asunto = models.CharField("Asunto del Correo", max_length=255)
    contenido_html = models.TextField("Cuerpo del Mensaje")
    
    # Automatización
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    programada_para = models.DateTimeField(null=True, blank=True)
    enviada = models.BooleanField(default=False)

    # Analítica (Lo que hace poderoso al sistema)
    total_enviados = models.PositiveIntegerField(default=0)
    aperturas_unicas = models.PositiveIntegerField(default=0)
    clicks_totales = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

class TrackingCorreo(models.Model):
    """Registra cada interacción individual"""
    campaña = models.ForeignKey(CampañaPro, on_delete=models.CASCADE, related_name='trackings')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    abierto = models.BooleanField(default=False)
    fecha_apertura = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.campaña.titulo} - {self.usuario.email}"
