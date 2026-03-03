import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, Post, Comment
from .forms import ContactForm

def services_list(request):
    servicios = Service.objects.filter(is_active=True)
    return render(request, 'agency/services_list.html', {'servicios': servicios})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mensaje_obj = form.save()
            
            token_telegram = "TU_TOKEN_DE_TELEGRAM_AQUI" 
            chat_id_telegram = "TU_CHAT_ID_AQUI"
            
            texto_tg = (
                f"🚀 *NUEVO LEAD - MD CHILE*\n\n"
                f"👤 *Nombre:* {mensaje_obj.name}\n"
                f"📧 *Email:* {mensaje_obj.email}\n"
                f"📝 *Mensaje:* {mensaje_obj.message}\n\n"
                f"📅 _Enviado el: {mensaje_obj.created_at.strftime('%d/%m/%Y %H:%M')}_"
            )
            
            url_tg = f"https://api.telegram.org/bot{token_telegram}/sendMessage"
            params_tg = {
                'chat_id': chat_id_telegram,
                'text': texto_tg,
                'parse_mode': 'Markdown'
            }
            
            try:
                send_mail(
                    f'Nuevo contacto de {mensaje_obj.name}',
                    f'Recibiste un mensaje de {mensaje_obj.email}: {mensaje_obj.message}',
                    settings.EMAIL_HOST_USER,
                    ['conversemos@marketingdigitalchile.cl'],
                    fail_silently=True,
                )
                requests.post(url_tg, data=params_tg)
            except Exception as e:
                print(f"Error en notificaciones: {e}")

            return render(request, 'agency/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'agency/contact_form.html', {'form': form})

def service_detail(request, slug):
    servicio = get_object_or_404(Service, slug=slug, is_active=True)
    reels_ids = []
    if servicio.reels_links:
        reels_ids = [r.strip() for r in servicio.reels_links.split(',')]
    
    if servicio.video_url:
        video_id = ""
        if "v=" in servicio.video_url:
            video_id = servicio.video_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in servicio.video_url:
            video_id = servicio.video_url.split("/")[-1]
        if video_id:
            servicio.video_url = f"https://www.youtube.com/embed/{video_id}?rel=0"

    return render(request, 'agency/service_detail.html', {
        'servicio': servicio,
        'reels': reels_ids
    })

# --- NUEVO: VISTA PARA AGREGAR COMENTARIOS ---
def add_comment(request, post_id):
    if request.method == "POST" and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            # Actualizamos el contador del post
            post.comments_count = post.comments_list.count()
            post.save()
        return redirect('blog_detail', slug=post.slug)
    return redirect('blog_list')

# agency/views.py

def privacidad(request):
    """Renderiza la página de política de privacidad."""
    return render(request, 'legal/privacidad.html')

def terminos(request):
    """Renderiza la página de términos y condiciones."""
    return render(request, 'legal/terminos.html')
