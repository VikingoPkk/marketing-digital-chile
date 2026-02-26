import requests
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Service
from .forms import ContactForm

def services_list(request):
    """Muestra todos los servicios activos para todos los usuarios."""
    servicios = Service.objects.filter(is_active=True)
    return render(request, 'agency/services_list.html', {'servicios': servicios})

def contact_view(request):
    """Procesa el formulario de contacto y envía notificaciones."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Guardamos el mensaje en la base de datos
            mensaje_obj = form.save()
            
            # --- CONFIGURACIÓN DE NOTIFICACIONES ---
            
            # 1. NOTIFICACIÓN POR TELEGRAM
            # Reemplaza con tus datos reales obtenidos de @BotFather y @userinfobot
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
            
            # 2. NOTIFICACIÓN POR EMAIL (OPCIONAL)
            try:
                # Envía un aviso a tu correo corporativo
                send_mail(
                    f'Nuevo contacto de {mensaje_obj.name}',
                    f'Recibiste un mensaje de {mensaje_obj.email}: {mensaje_obj.message}',
                    settings.EMAIL_HOST_USER,
                    ['conversemos@marketingdigitalchile.cl'], # Cambia por tu email real
                    fail_silently=True,
                )
                # Intentamos enviar el mensaje a Telegram
                requests.post(url_tg, data=params_tg)
            except Exception as e:
                print(f"Error en notificaciones: {e}")

            return render(request, 'agency/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'agency/contact_form.html', {'form': form})

def service_detail(request, slug):
    """Muestra el detalle de un servicio con video y reels procesados."""
    servicio = get_object_or_404(Service, slug=slug, is_active=True)
    
    # Procesamos los IDs de Reels (asumiendo formato: id1, id2, id3)
    reels_ids = []
    if servicio.reels_links:
        reels_ids = [r.strip() for r in servicio.reels_links.split(',')]
    
    # Limpieza de URL de YouTube para que sea compatible con Iframe (Embed)
    if servicio.video_url:
        video_id = ""
        if "v=" in servicio.video_url:
            # Caso: youtube.com/watch?v=XXXXXX
            video_id = servicio.video_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in servicio.video_url:
            # Caso: youtu.be/XXXXXX
            video_id = servicio.video_url.split("/")[-1]
            
        if video_id:
            servicio.video_url = f"https://www.youtube.com/embed/{video_id}?rel=0"

    return render(request, 'agency/service_detail.html', {
        'servicio': servicio,
        'reels': reels_ids
    })
