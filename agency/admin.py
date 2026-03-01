from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Service, ContactMessage, Project, HomeSection, HomeReel, ClientLogo, UserTestimonial

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
    list_display = ('name', 'rating')

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
    change_list_template = "admin/agency/contactmessage/change_list.html"