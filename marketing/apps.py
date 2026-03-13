from django.apps import AppConfig

class MarketingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketing'
    verbose_name = 'EMAIL MARKETING' # Así aparecerá en el menú lateral
