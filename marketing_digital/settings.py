import os
from pathlib import Path

# Construye las rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de desarrollo
SECRET_KEY = 'django-insecure-^3_ttqv8tsxw9fc80*d=#4)b*frt3grya(_w^sx#re9nbn#0eo'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Aplicaciones
INSTALLED_APPS = [
    'jazzmin',  # <--- JAZZMIN SIEMPRE DEBE IR PRIMERO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'corsheaders',
    'import_export', 
    'rest_framework',
    'agency',  
    'users',   
    'courses',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework_simplejwt',
    'marketing', # Nuestra nueva app de Mailchimp casero
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'marketing_digital.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'marketing_digital.wsgi.application'

# --- BASE DE DATOS ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# --- CONFIGURACIÓN DE ALLAUTH ---
SITE_ID = 1
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none' 

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Internacionalización
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Estáticos y Media
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'users.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 

# Permite que el navegador renderice iframes correctamente
X_FRAME_OPTIONS = 'SAMEORIGIN'

# =============================================================================
# CONFIGURACIÓN DE JAZZMIN (DISEÑO PREMIUM DEL ADMIN)
# =============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "MD Chile Admin",
    "site_header": "Marketing Digital Chile",
    "site_brand": "MD CHILE",
    "welcome_sign": "Bienvenido al Centro de Comando, Angelo",
    "copyright": "Marketing Digital Chile",
    "search_model": ["agency.Post", "courses.Course"],
    "user_avatar": "profile_picture",

    # --- NOTIFICACIONES EN EL MENÚ ---
    "menu_count": [
        {
            "model": "agency.contactmessage", 
            "func": lambda obj: obj.objects.filter(is_read=False).count() 
        }
    ],

    # --- ICONOS DE PESTAÑAS ---
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "users.User": "fas fa-user-friends",
        "agency.Post": "fas fa-blog",
        "agency.Service": "fas fa-rocket",
        "agency.Project": "fas fa-code",
        "agency.ContactMessage": "fas fa-envelope-open-text",
        "courses.Course": "fas fa-graduation-cap",
        "courses.Lesson": "fas fa-play-circle",
        "courses.Enrollment": "fas fa-user-graduate",
        # Icono para la nueva app de Marketing
        "marketing.CampañaPro": "fas fa-paper-plane",
        "marketing.TrackingCorreo": "fas fa-chart-bar",
    },
    
    # --- ORDEN DE LAS PESTAÑAS (Aquí aparece EMAIL MARKETING) ---
    "sidebar_order": [
        "auth", 
        "users", 
        "marketing",  # Pestaña de Email Marketing visible
        "courses", 
        "agency"
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    
    # --- LINKS SUPERIORES ---
    "top_links": [
        {"name": "Inicio", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Analítica de Marketing", "url": "marketing_stats"}, # Acceso directo a tu Dashboard
    ],

    "show_ui_builder": True, 

    # settings.py dentro de JAZZMIN_SETTINGS
    "custom_links": {
        "marketing": [ # Debajo de la app marketing aparecerá este botón
            {
                "name": "Redactar Nueva Campaña", 
                "url": "/admin/users/user/", 
                "icon": "fas fa-paper-plane",
                "permissions": ["auth.view_user"]
            },
        ],
    },
}

JAZZMIN_UI_CONFIG = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False, 
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly", 
    "dark_mode_theme": "darkly", 
} 

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# PROTOCOLO DE ENVÍO DE CORREOS (GMAIL)
# =============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'oncocit2@gmail.com'
EMAIL_HOST_PASSWORD = 'nixqpuwqttggulgy'
DEFAULT_FROM_EMAIL = 'Marketing Digital Chile <oncocit2@gmail.com>'

# URL base para el tracking de imágenes y clicks
SITE_URL = "http://127.0.0.1:8000"