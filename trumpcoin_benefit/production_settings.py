"""
Production settings for TrumpCoin Benefit project.
This file contains settings that are specific to the production environment.
"""

from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(lucxc%komz04$r0v!twbgz(ztfk^n5ko(y&mc(c%gz%f1+y3-'  # TODO: Generate a new secure key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['trumpcoin-benefit-2oyf.onrender.com', 'trumpcoin-benefit.live', 'www.trumpcoin-benefit.live', 'localhost', '127.0.0.1']  # TODO: Add your domain

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# PostgreSQL configuration (recommended for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trumpcoin_cnuv',
        'USER': 'trumpcoin_user',
        'PASSWORD': '19Xxp0GAWLSWsfgvlVlkBTDYyVcqESJV',
        'HOST': 'dpg-d0p3j36uk2gs739903e0-a.oregon-postgres.render.com',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
    }
}

# Email configuration
# Email configuration (using Zoho Mail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('ZOHO_EMAIL_USER', 'admin@trumpcoin-benefit.live')  # your full Zoho email address
EMAIL_HOST_PASSWORD = os.environ.get('ZOHO_EMAIL_PASSWORD', 'Qt9xkQf5tkES')  # your Zoho email password or app password
DEFAULT_FROM_EMAIL = 'TrumpCoin Benefit <noreply@trumpcoin-benefit.live>'


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/error.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'benefit': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Create logs directory if it doesn't exist
import os
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
