from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Optional dev-specific apps
INSTALLED_APPS += [
    "django_extensions",  # for shell_plus, runserver_plus, etc.
]

# Dev DB override (optional)
DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}