from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import UserTestimonial, HomeSection, HomeReel, ClientLogo, Service, ContactMessage, Project, Post, Comment

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
    actions = ['approve_testimonials', 'reject_testimonials']

    @admin.action(description="Aprobar testimonios")
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Reprobar testimonios")
    def reject_testimonials(self, request, queryset):
        queryset.update(is_approved=False)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin): 
    list_display = ('name', 'email', 'servicio_interes', 'is_read', 'created_at')
    list_filter = ('is_read', 'servicio_interes', 'created_at')
    actions = ['mark_as_read']

    @admin.action(description="Marcar como LEÍDOS")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Información', {'fields': ('title', 'slug', 'author', 'is_published')}),
        ('Visual', {'fields': ('image', 'video_url')}),
        ('Contenido', {'fields': ('content',)}),
        ('Métricas', {'fields': ('likes_count', 'comments_count', 'reading_time'), 'classes': ('collapse',)}),
    ) 

# agency/admin.py

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username', 'post__title')