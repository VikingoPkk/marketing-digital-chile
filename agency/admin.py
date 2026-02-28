from django.contrib import admin
from import_export.admin import ImportExportModelAdmin # <-- HERRAMIENTA DE EXCEL
from .models import Service, ContactMessage

# Registro para que aparezcan los Servicios
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

# Registro para que aparezcan los Mensajes de Contacto (BLINDADO)
@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin): 
    # Agregamos campos adicionales para que Angelo tenga más contexto rápido
    list_display = ('name', 'email', 'servicio_interes', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('name', 'email', 'message')
    list_filter = ('servicio_interes', 'created_at')

    # --- INTEGRACIÓN DEL DASHBOARD PROFESIONAL ---
    change_list_template = "admin/agency/contactmessage/change_list.html"
