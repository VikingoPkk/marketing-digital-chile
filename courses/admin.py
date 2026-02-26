from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, LessonProgress, Quiz, Question

# Configuración para agregar preguntas directamente dentro del Quiz
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3  # Te muestra 3 espacios vacíos para preguntas nuevas por defecto

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module')
    inlines = [QuestionInline]

# Registro de los modelos base
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'price')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')

admin.site.register(Enrollment)
admin.site.register(LessonProgress)
