from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Modelo de Curso con Imagen Editable
class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    # Campo para la imagen que verás en el Dashboard
    image = models.ImageField(upload_to='courses/banners/', null=True, blank=True)
    price = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def total_lessons(self):
        return Lesson.objects.filter(module__course=self).count()

# Organización por Módulos
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# Lecciones del curso
class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

# Matrícula de alumnos
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

# Registro de progreso (Botón Completar)
class LessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson')

# Sistema de Exámenes
class Quiz(models.Model):
    module = models.OneToOneField(Module, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    correct_option = models.IntegerField(choices=[(1, 'Opción 1'), (2, 'Opción 2'), (3, 'Opción 3')])