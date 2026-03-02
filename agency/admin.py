from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import UserTestimonial, HomeSection, HomeReel, ClientLogo, Service, ContactMessage, Project

@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ('section_type', 'title', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(HomeReel)
class HomeReelAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(UserTestimonial)
class UserTestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('name', 'comment')
    actions = ['approve_testimonials', 'reject_testimonials']

    @admin.action(description="Aprobar testimonios (Publicar en Home)")
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Los testimonios seleccionados han sido aprobados.")

    @admin.action(description="Reprobar testimonios (Quitar del Home)")
    def reject_testimonials(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Los testimonios seleccionados han sido ocultados.")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin): 
    list_display = ('name', 'email', 'servicio_interes', 'created_at')
    # Nota: Asegúrate de tener este archivo creado o comenta la línea de abajo si da error
    # change_list_template = "admin/agency/contactmessage/change_list.html"