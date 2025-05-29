import os
import dj_database_url
from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-(lucxc%komz04$r0v!twbgz(ztfk^n5ko(y&mc(c%gz%f1+y3-')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Keep debug enabled to help diagnose 500 errors

# ALLOWED_HOSTS = ['trumpcoin-benefit.onrender.com', 'trumpcoin-benefit.live', 'www.trumpcoin-benefit.live']
import os

# Get the ALLOWED_HOSTS from environment variable or use default
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'trumpcoin-benefit-2oyf.onrender.com,localhost,127.0.0.1,trumpcoin-benefit.live,www.trumpcoin-benefit.live').split(',')

# Set RENDER environment variable to indicate we're running on Render.com
os.environ['RENDER'] = 'true'

# Add context processor for base template selection
TEMPLATES[0]['OPTIONS']['context_processors'].append('benefit.context_processors.base_template')


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Get DATABASE_URL from environment variable with fallback to your manual database
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://trumpcoin_user:19Xxp0GAWLSWsfgvlVlkBTDYyVcqESJV@dpg-d0p3j36uk2gs739903e0-a.oregon-postgres.render.com/trumpcoin_cnuv')
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


# Simplified static file serving
# Use the simpler StaticFilesStorage instead of CompressedManifestStaticFilesStorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# WhiteNoise debugging settings
WHITENOISE_AUTOREFRESH = True  # Refresh static files on each request
WHITENOISE_USE_FINDERS = True  # Use Django's finders to locate static files

# Make sure WhiteNoise middleware is first after security middleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Disable HTTPS settings temporarily for troubleshooting
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Email configuration (using SendGrid as an example)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Use console backend for testing
# Email configuration (using Zoho Mail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('ZOHO_EMAIL_USER', 'admin@trumpcoin-benefit.live')  # your full Zoho email address
EMAIL_HOST_PASSWORD = os.environ.get('ZOHO_EMAIL_PASSWORD', 'Qt9xkQf5tkES')  # your Zoho email password or app password
DEFAULT_FROM_EMAIL = 'TrumpCoin Benefit <noreply@trumpcoin-benefit.live>'


# Enhanced logging configuration for debugging
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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',  # Set to DEBUG to see all SQL queries
            'propagate': False,
        },
        'benefit': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
