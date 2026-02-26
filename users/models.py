from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Ya tienes estos campos, los mantenemos
    is_client = models.BooleanField(default=True) # Por defecto todos son clientes
    is_admin_user = models.BooleanField(default=False)
    
    # Nuevos campos para el perfil
    profile_picture = models.ImageField(upload_to='users/profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    rut = models.CharField(max_length=12, blank=True, null=True) # Importante para facturación en Chile
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.email}"
