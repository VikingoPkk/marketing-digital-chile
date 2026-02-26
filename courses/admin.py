from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment

# Permite agregar lecciones dentro de la vista del módulo
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'video_url', 'order') # Aquí aparecerá el campo de video

# Permite agregar módulos dentro de la vista del curso
class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1
    show_change_link = True

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_published')
    search_fields = ('title',)
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [LessonInline] # <--- AQUÍ ES DONDE AGREGARÁS LOS VIDEOS

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
