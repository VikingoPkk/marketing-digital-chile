from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from .models import CampañaPro, TrackingCorreo

def ejecutar_lanzamiento(datos_formulario, alumnos_queryset):
    """
    Recibe los datos del editor HTML y la lista de alumnos a los que enviar.
    """
    # 1. Registramos la campaña en la base de datos de marketing
    nueva_campaña = CampañaPro.objects.create(
        titulo=f"Campaña: {datos_formulario['asunto']}",
        asunto=datos_formulario['asunto'],
        contenido_html=datos_formulario['cuerpo'],
    )

    for alumno in alumnos_queryset:
        # 2. Creamos el registro de tracking para este alumno específico
        tracking = TrackingCorreo.objects.create(
            campaña=nueva_campaña,
            usuario=alumno
        )

        # 3. Construimos los links dinámicos usando SITE_URL
        pixel_url = f"{settings.SITE_URL}/t/open/{tracking.id}/pixel.gif"
        click_url = f"{settings.SITE_URL}/t/click/{tracking.id}/"

        # 4. Inyectamos el tracking en el contenido
        # Sustituimos la URL de destino del botón por nuestro link de tracking
        contenido_personalizado = datos_formulario['cuerpo'].replace(
            datos_formulario['url_destino'], click_url
        )
        # Agregamos el pixel invisible al final
        contenido_personalizado += f'<img src="{pixel_url}" width="1" height="1" style="display:none !important;" />'

        # 5. Envío Real
        msg = EmailMultiAlternatives(
            nueva_campaña.asunto,
            strip_tags(contenido_personalizado),
            settings.DEFAULT_FROM_EMAIL,
            [alumno.email]
        )
        msg.attach_alternative(contenido_personalizado, "text/html")
        msg.send()

        # Actualizamos contadores
        nueva_campaña.total_enviados += 1
    
    nueva_campaña.enviada = True
    nueva_campaña.save()
    return nueva_campaña