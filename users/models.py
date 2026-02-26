from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Campos de roles
    is_client = models.BooleanField(default=True) 
    is_admin_user = models.BooleanField(default=False)
    
    # Perfil y Personalización
    profile_picture = models.ImageField(upload_to='users/profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Datos específicos para Chile y Redes
    rut = models.CharField(max_length=12, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.email}"
