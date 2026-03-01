import os
import dj_database_url
from .base import *

# 1. Security First
DEBUG = False
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") # Ensure this is unique in prod
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ".render.com,.railway.app").split(",")

# 2. Database Configuration
# Using dj_database_url allows it to work automatically with 'DATABASE_URL' env var
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# 3. Static & Media Files (WhiteNoise)
# This allows Django to serve its own static files without Nginx
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 4. HTTPS & Security Headers
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True") == "True"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS Settings (Add only after verifying SSL works)
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 5. Production Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}