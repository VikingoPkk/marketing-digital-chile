from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, LessonProgress, Quiz, Question, Certificate, CourseQuery

# 1. Configuración para agregar preguntas directamente dentro del Quiz
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3  # Te muestra 3 espacios vacíos para preguntas nuevas por defecto

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module')
    inlines = [QuestionInline]

# 2. Registro de los modelos base con personalización
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

# 3. Registro de Consultas Académicas (Opción A)
@admin.register(CourseQuery)
class CourseQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'lesson', 'created_at', 'is_answered')
    list_filter = ('course', 'created_at')
    search_fields = ('user__username', 'question')

    def is_answered(self, obj):
        return bool(obj.answer)
    is_answered.boolean = True
    is_answered.short_description = '¿Respondida?'

# 4. Modelos adicionales registrados de forma simple
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(Certificate)