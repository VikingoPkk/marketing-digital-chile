from django.db import models
from django.utils.text import slugify

# Mantén tu modelo Service arriba...
class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre del Servicio")
    slug = models.SlugField(unique=True, blank=True)
    icon_emoji = models.CharField(max_length=10, default="🚀")
    short_description = models.TextField(max_length=300)
    long_description = models.TextField()
    banner_image = models.ImageField(upload_to='services/banners/')
    video_url = models.URLField(blank=True, null=True)
    reels_links = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# NUEVO MODELO PARA CONTACTO (Asegúrate de la sangría aquí abajo)
class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    message = models.TextField(verbose_name="Mensaje o Consulta")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.name} - {self.email}"