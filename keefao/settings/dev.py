from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Optional dev-specific apps
INSTALLED_APPS += [
    "django_extensions",  # for shell_plus, runserver_plus, etc.
]

# Dev DB override
DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

# Log M-Pesa & Stripe requests to the console during dev
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "payments": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Email Backend for local testing (prints emails to console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"