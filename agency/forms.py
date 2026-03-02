from django import forms
from .models import ContactMessage, UserTestimonial

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'tu@email.com'}),
            'message': forms.Textarea(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-blue-500 h-32', 'placeholder': '¿Cómo podemos ayudarte?'}),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = UserTestimonial
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'w-full p-3 bg-gray-50 rounded-xl border-none focus:ring-2 focus:ring-yellow-500'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full p-3 bg-gray-50 rounded-xl border-none focus:ring-2 focus:ring-yellow-500 h-24',
                'placeholder': 'Cuéntanos tu experiencia (máximo 300 caracteres)...',
                'maxlength': '300'
            }),
        }