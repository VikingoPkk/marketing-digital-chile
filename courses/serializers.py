from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Lesson 

# Definimos el modelo de usuario activo en el sistema
User = get_user_model()

class LessonSerializer(serializers.ModelSerializer):
    """Protocolo de traducción para lecciones individuales."""
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'video_url']

class CursoSerializer(serializers.ModelSerializer):
    """Protocolo para lista de cursos y tienda con URLs absolutas para la App."""
    image = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'image', 'price']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class UserSerializer(serializers.ModelSerializer):
    """Sincronizador: Extrae la foto del carpincho y el nombre de Angelo Wilche H."""
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        # Aseguramos que estos campos existan para evitar el error de 'oncocit2'
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'foto_url']

    def get_foto_url(self, obj):
        # Verificamos si el usuario tiene el campo profile_picture (el del carpincho)
        if hasattr(obj, 'profile_picture') and obj.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None