from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """Divide una cadena por la clave dada."""
    return value.split(key)

@register.filter(name='modulo')
def modulo(num, val):
    """Devuelve el resto de la división."""
    return num % val

@register.filter(name='trim')
def trim(value):
    """Limpia espacios en blanco."""
    return value.strip() 