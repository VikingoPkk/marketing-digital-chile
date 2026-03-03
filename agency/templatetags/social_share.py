# agency/templatetags/social_share.py
from django import template
from urllib.parse import quote

register = template.Library()

@register.simple_tag
def share_link(platform, url, title):
    """Genera enlaces de compartir dinámicos para el blog."""
    encoded_url = quote(url)
    encoded_title = quote(title)
    
    links = {
        'facebook': f'https://www.facebook.com/sharer/sharer.php?u={encoded_url}',
        'twitter': f'https://twitter.com/intent/tweet?url={encoded_url}&text={encoded_title}',
        'linkedin': f'https://www.linkedin.com/shareArticle?mini=true&url={encoded_url}&title={encoded_title}',
        'whatsapp': f'https://api.whatsapp.com/send?text={encoded_title}%20{encoded_url}',
    }
    
    return links.get(platform, '#')