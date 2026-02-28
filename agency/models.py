from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    # --- TUS CAMPOS ORIGINALES ---
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

    # --- AGREGADO: CAMPOS PARA LEAD MAGNET (EL REGALO) ---
    # Estos campos permitirán que la página de gracias entregue el botín automáticamente
    regalo_pdf = models.FileField(upload_to='leads/pdfs/', blank=True, null=True, verbose_name="Ebook o Guía PDF de Regalo")
    regalo_video_privado = models.URLField(blank=True, null=True, verbose_name="URL Video Privado (YouTube/Vimeo)")
    cta_regalo_text = models.CharField(max_length=100, default="¡Descargar mi regalo ahora!", verbose_name="Texto del Botón de Regalo")

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    # --- TUS CAMPOS ORIGINALES ---
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    message = models.TextField(verbose_name="Mensaje o Consulta")
    created_at = models.DateTimeField(auto_now_add=True)

    # --- AGREGADO: INTELIGENCIA DE CONVERSIÓN ---
    # Para saber qué servicio específico generó el contacto en la landing
    servicio_interes = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Servicio de Interés"
    )
    # Para identificar si el lead viene de Meta Suite u otro origen
    lead_source = models.CharField(
        max_length=100, 
        default="Web Directa", 
        verbose_name="Origen del Lead"
    )

    def __str__(self):
        return f"Lead: {self.name} - Interesado en: {self.servicio_interes}" 
    
    # agency/models.py
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título del Proyecto")
    description = models.TextField(verbose_name="Descripción")
    image = models.ImageField(upload_to='projects/', verbose_name="Imagen del Software")
    url_demo = models.URLField(blank=True, null=True, verbose_name="Enlace Demo/Web")
    technologies = models.CharField(max_length=200, verbose_name="Tecnologías usadas")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['order']

    def __str__(self):
        return self.title