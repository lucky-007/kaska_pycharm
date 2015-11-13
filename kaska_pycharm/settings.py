import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open('/home/u49036/secret_key/key.txt') as f:
    SECRET_KEY = f.read().strip()

DEBUG = False


SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 1800
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'


AUTH_USER_MODEL = 'players.Player'
LOGIN_URL = '/players/login'
LOGIN_REDIRECT_URL = '/'


ALLOWED_HOSTS = [
    '.kaska.me',
]


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'players'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  # do we really need it?
)

ROOT_URLCONF = 'kaska_pycharm.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'kaska_pycharm.wsgi.application'

with open('/home/u49036/secret_key/db_password.txt') as f:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'u49036',
            'USER': 'u49036',
            'HOST': '127.0.0.1',
            'PASSWORD': f.read().strip(),
        }
    }


LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'kaska.me'
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'info@kaska.me'
EMAIL_HOST_PASSWORD = 'dolgogern2015'
EMAIL_PORT = 25  # 1025


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'files', 'static_collected')
MEDIA_ROOT = os.path.join(BASE_DIR, 'files', 'media')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'files', 'static'),
)
