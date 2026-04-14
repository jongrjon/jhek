"""Production settings. Intentionally strict — all secrets from env."""

import os

from .base import *  # noqa: F401,F403
from .base import env

DEBUG = False

# ALLOWED_HOSTS from env. Also accept Render's auto-set hostname.
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_hostname and render_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_hostname)
if not ALLOWED_HOSTS:
    raise RuntimeError("ALLOWED_HOSTS must be set in production.")

# SECRET_KEY must be set via env — do not accept the base default.
SECRET_KEY = env("SECRET_KEY")

# WhiteNoise — serve static files from the Django process.
# Insert after SecurityMiddleware (index 0 → position 1).
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Security hardening.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=60 * 60 * 24 * 30)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# Log rejected hosts so 400 errors are diagnosable.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    },
}
