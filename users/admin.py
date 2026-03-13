from django.contrib import admin
from django.shortcuts import render
from .models import User

@admin.register(User)
class MyUserAdmin(admin.ModelAdmin): # O UserAdmin si heredas del original
    actions = ['enviar_email_personalizado']

    def enviar_email_personalizado(self, request, queryset):
        return render(request, 'admin/enviar_email_form.html', {'users': queryset})
    
    enviar_email_personalizado.short_description = "✍️ Redactar y enviar Email Marketing"