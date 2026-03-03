from rest_framework import serializers
from .models import Course, Lesson # Importamos ambos modelos para la academia

class LessonSerializer(serializers.ModelSerializer):
    """Protocolo de traducción para lecciones individuales."""
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'video_url']

class CursoSerializer(serializers.ModelSerializer):
    """Protocolo de traducción para la lista de cursos."""
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'image']