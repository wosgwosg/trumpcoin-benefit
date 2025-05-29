"""
Fixed Render.com settings for TrumpCoin Benefit project.
This file contains optimized settings for PostgreSQL database connection on Render.com
"""
import os
import dj_database_url
from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-(lucxc%komz04$r0v!twbgz(ztfk^n5ko(y&mc(c%gz%f1+y3-')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Set to True temporarily for debugging database issues

# Get the ALLOWED_HOSTS from environment variable or use default
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'trumpcoin-benefit-2oyf.onrender.com,localhost,127.0.0.1,trumpcoin-benefit.live,www.trumpcoin-benefit.live').split(',')

# Set RENDER environment variable to indicate we're running on Render.com
os.environ['RENDER'] = 'true'

# Add context processor for base template selection
TEMPLATES[0]['OPTIONS']['context_processors'].append('benefit.context_processors.base_template')

# Database Configuration
# Multiple fallback options for database connection
DATABASE_URL = os.environ.get('DATABASE_URL')

# If no DATABASE_URL environment variable, use your manual database configuration
if not DATABASE_URL:
    # Your manual database configuration from screenshot
    DATABASE_URL = 'postgresql://trumpcoin_user:19Xxp0GAWLSWsfgvlVlkBTDYyVcqESJV@dpg-d0p3j36uk2gs739903e0-a.oregon-postgres.render.com/trumpcoin_cnuv'

# Configure database with enhanced settings for Render.com
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,  # Keep connections alive for 10 minutes
        conn_health_checks=True,  # Enable connection health checks
        ssl_require=True,  # Require SSL for security
    )
}

# Alternative manual database configuration (commented out, use if dj_database_url fails)
"""
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
"""

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Simplified static file serving for Render.com
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# WhiteNoise configuration for static files
WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True

# Ensure WhiteNoise middleware is properly positioned
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Security settings (temporarily disabled for debugging)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Email configuration (using Zoho Mail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('ZOHO_EMAIL_USER', 'admin@trumpcoin-benefit.live')
EMAIL_HOST_PASSWORD = os.environ.get('ZOHO_EMAIL_PASSWORD', 'Qt9xkQf5tkES')
DEFAULT_FROM_EMAIL = 'TrumpCoin Benefit <noreply@trumpcoin-benefit.live>'

# Enhanced logging configuration for database debugging
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
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Enable to see all SQL queries and connection details
            'propagate': False,
        },
        'benefit': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Database connection timeout settings
DATABASE_CONNECTION_TIMEOUT = 30
DATABASE_QUERY_TIMEOUT = 30

print("🔧 Render settings loaded with PostgreSQL configuration")
print(f"📊 Database URL configured: {'✅ Yes' if DATABASE_URL else '❌ No'}")
print(f"🔗 Database Host: {DATABASES['default'].get('HOST', 'Not configured')}")
