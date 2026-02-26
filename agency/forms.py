from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'tu@email.com'}),
            'message': forms.Textarea(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-blue-500 h-32', 'placeholder': '¿Cómo podemos ayudarte?'}),
        }