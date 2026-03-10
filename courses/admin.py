from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Course, Module, Lesson, Enrollment, LessonProgress, Quiz, Question, Certificate, CourseQuery

User = get_user_model()

# ==========================================
# ACCIONES DE MARKETING PRO CON SOPORTE HTML
# ==========================================

@admin.action(description='✍️ Redactar y enviar Email Marketing')
def enviar_campana_personalizada(modeladmin, request, queryset):
    if 'apply' in request.POST:
        asunto = request.POST.get('subject')
        # El mensaje capturado puede contener etiquetas HTML enviadas por el usuario
        mensaje_html_usuario = request.POST.get('message')
        texto_boton = request.POST.get('button_text', 'VOLVER A MIS CURSOS')
        url_boton = request.POST.get('button_url', 'https://mdchile.cl/dashboard/')
        doc_url = request.POST.get('document_url')
        video_url = request.POST.get('video_url')
        
        count = 0
        for usuario in queryset:
            if usuario.email:
                contexto = {
                    'first_name': usuario.first_name or usuario.username,
                    'mensaje_personalizado': mensaje_html_usuario, # Se pasa íntegro a la plantilla
                    'texto_boton': texto_boton,
                    'url_boton': url_boton,
                    'doc_url': doc_url,
                    'video_url': video_url
                }
                # Se renderiza la plantilla envolviendo el HTML del usuario
                html_final = render_to_string('emails/marketing_campaing.html', contexto)
                
                send_mail(
                    subject=asunto,
                    message=strip_tags(html_final), # Versión texto plano para evitar SPAM
                    from_email=None, 
                    recipient_list=[usuario.email],
                    html_message=html_final, # Versión HTML para el diseño premium
                )
                count += 1
                
        modeladmin.message_user(request, f"Campaña '{asunto}' enviada con éxito a {count} usuarios.")
        return HttpResponseRedirect(request.get_full_path())

    return render(request, 'admin/enviar_email_form.html', context={
        'users': queryset,
        'title': 'Redactar Campaña de Marketing'
    })

# --- EL RESTO DEL ARCHIVO SE MANTIENE IGUAL ---
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module')
    inlines = [QuestionInline]

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

@admin.register(CourseQuery)
class CourseQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'lesson', 'created_at', 'is_answered')
    list_filter = ('course', 'created_at')
    search_fields = ('user__username', 'question')

    def is_answered(self, obj):
        return bool(obj.answer)
    is_answered.boolean = True
    is_answered.short_description = '¿Respondida?'

admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(Certificate)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    actions = [enviar_campana_personalizada]
    search_fields = ('username', 'email', 'first_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')