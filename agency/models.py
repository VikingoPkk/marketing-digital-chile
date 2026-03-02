from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator

# --- 1. ESTRUCTURA MODULAR DEL HOME ---
class HomeSection(models.Model):
    SECTION_TYPES = (
        ('hero', 'Sección Principal (Hero)'),
        ('reels', 'Sección de Reels/Videos'),
        ('clients', 'Logos de Clientes'),
        ('testimonials', 'Testimonios de Usuarios'),
        ('services_preview', 'Resumen de Servicios'),
    )
    title = models.CharField(max_length=200, verbose_name="Texto/Subtítulo de la sección")
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="¿Mostrar en el Home?")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden de aparición")

    class Meta:
        ordering = ['order']
        verbose_name = "Estructura del Home"
        verbose_name_plural = "Estructura del Home"

    def __str__(self):
        return f"{self.get_section_type_display()} - {self.title}"

# --- 2. CONTENIDO EDITABLE DEL HOME ---
class HomeReel(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título del Reel")
    video_url = models.URLField(verbose_name="Link del Video (Instagram/TikTok/YouTube)")
    thumbnail = models.ImageField(upload_to='reels/thumbs/', verbose_name="Portada del Reel")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ClientLogo(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de la Empresa")
    logo = models.ImageField(upload_to='clients/', verbose_name="Foto/Logo del Cliente")
    url_web = models.URLField(blank=True, null=True, verbose_name="Enlace a su sitio web")
    
    def __str__(self):
        return self.name

class UserTestimonial(models.Model):
    # Relación dinámica con el usuario (Soluciona error E301 de tu terminal)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="testimonios",
        verbose_name="Alumno"
    )
    name = models.CharField(max_length=100, verbose_name="Nombre para mostrar")
    comment = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(300)],
        verbose_name="Reseña (Máx 300 caracteres)"
    )
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)], verbose_name="Estrellas")
    is_approved = models.BooleanField(default=False, verbose_name="¿Aprobado para el Home?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de envío")

    class Meta:
        verbose_name = "Testimonio de Usuario"
        verbose_name_plural = "Testimonios de Usuarios"

    def __str__(self):
        return f"{self.name} - {self.rating} Estrellas"

# --- 3. SERVICIOS, PROYECTOS Y LEADS ---
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
    regalo_pdf = models.FileField(upload_to='leads/pdfs/', blank=True, null=True, verbose_name="Ebook PDF de Regalo")
    regalo_video_privado = models.URLField(blank=True, null=True, verbose_name="URL Video Privado")
    cta_regalo_text = models.CharField(max_length=100, default="¡Descargar mi regalo ahora!", verbose_name="Texto del Botón")

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    message = models.TextField(verbose_name="Mensaje")
    created_at = models.DateTimeField(auto_now_add=True)
    servicio_interes = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    lead_source = models.CharField(max_length=100, default="Web Directa")

    def __str__(self):
        return f"Lead: {self.name}"

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    url_demo = models.URLField(blank=True, null=True)
    technologies = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.title