from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from .models import CampañaPro, TrackingCorreo

def procesar_y_enviar_campaña(campaña_id, lista_usuarios):
    campaña = CampañaPro.objects.get(id=campaña_id)
    
    for usuario in lista_usuarios:
        # 1. Creamos el registro de tracking para este usuario
        tracking = TrackingCorreo.objects.create(
            campaña=campaña,
            usuario=usuario
        )

        # 2. Personalizamos el contenido
        # Insertamos el Píxel de Apertura al final del HTML
        pixel_url = f"{settings.SITE_URL}/t/open/{tracking.id}/pixel.gif"
        pixel_tag = f'<img src="{pixel_url}" width="1" height="1" style="display:none !important;" />'
        
        # Reemplazamos el link del botón por el link de tracking de click
        # Buscamos una etiqueta especial que tú pongas en el editor, ej: {{LINK_CURSO}}
        click_url = f"{settings.SITE_URL}/t/click/{tracking.id}/"
        contenido_final = campaña.contenido_html.replace("{{LINK_CURSO}}", click_url)
        contenido_final += pixel_tag

        # 3. Enviar Correo
        subject = campaña.asunto
        from_email = settings.DEFAULT_FROM_EMAIL
        to = usuario.email
        text_content = strip_tags(contenido_final)
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(contenido_final, "text/html")
        msg.send()
        
        # 4. Actualizar contador de enviados
        campaña.total_enviados += 1
        campaña.save()