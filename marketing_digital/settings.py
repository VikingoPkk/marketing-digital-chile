import os
from pathlib import Path

# Construye las rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de desarrollo
SECRET_KEY = 'django-insecure-^3_ttqv8tsxw9fc80*d=#4)b*frt3grya(_w^sx#re9nbn#0eo'
DEBUG = True
ALLOWED_HOSTS = []

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
    'import_export', # <-- ARTILLERÍA DE EXPORTACIÓN 
    'rest_framework',
    'agency',  
    'users',   
    'courses',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # AGREGAR ESTO AQUÍ
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
ACCOUNT_SIGNUP_FIELDS = ['email', 'password1'] 
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

# Permite que el navegador renderice iframes correctamente (Para videos de YouTube)
X_FRAME_OPTIONS = 'SAMEORIGIN'

# --- CONFIGURACIÓN DE ENVÍO DE CORREOS ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_CHARSET = 'utf-8'
EMAIL_HOST_USER = 'oncocit2@gmail.com'
EMAIL_HOST_PASSWORD = 'nixqpuwqttggulgy'

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

    # --- ESTO ACTIVA EL NÚMERO DE NOTIFICACIÓN (+1 a +99) ---
    "menu_count": [
        {
            "model": "agency.contactmessage", # IMPORTANTE: En minúsculas aquí
            "func": lambda obj: obj.objects.filter(is_read=False).count() 
        }
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "agency.Post": "fas fa-blog",
        "agency.Service": "fas fa-rocket",
        "agency.Project": "fas fa-code",
        "agency.ContactMessage": "fas fa-envelope-open-text",
        "courses.Course": "fas fa-graduation-cap",
        "courses.Lesson": "fas fa-play-circle",
        "courses.Enrollment": "fas fa-user-graduate",
    },
    
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["agency", "courses", "auth"],
    "show_ui_builder": True, # <--- INTERRUPTOR MAESTRO PARA COMPONENTES DINÁMICOS
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