"""Development settings. Safe defaults for local work."""

from .base import *  # noqa: F401,F403
from .base import env

DEBUG = True
ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "0.0.0.0"])

# Do not require HTTPS in dev.
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Quieter default for dev.
if "SECRET_KEY" not in globals() or not globals().get("SECRET_KEY"):
    SECRET_KEY = "dev-only-insecure-key-change-me"
