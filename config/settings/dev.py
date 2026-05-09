from datetime import timedelta

from config.settings.base import *
from config.settings.base import env

SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

ADMIN_URL = env.str("ADMIN_URL", default="admin/")

# auth_system settings — override AUTH_SYSTEM.JWT_COOKIE_SECURE to False in dev
# so cookies work without HTTPS on localhost.
AUTH_SYSTEM = {
    "JWT_ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "JWT_REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "JWT_ACCESS_COOKIE_NAME": "access_token",
    "JWT_REFRESH_COOKIE_NAME": "refresh_token",
    "JWT_COOKIE_SECURE": False,  # set True in production (requires HTTPS)
    "JWT_COOKIE_SAMESITE": "Lax",
    "JWT_COOKIE_HTTPONLY": True,
    "REDIS_URL": env.str("REDIS_URL", default="redis://127.0.0.1:6379/0"),
    "PENDING_SESSION_TTL": 300,
    "PENDING_SESSION_PREFIX": "auth:pending:",
    "TOTP_ISSUER_NAME": env.str("TOTP_ISSUER_NAME", default="Nexora"),
    "BACKUP_CODES_COUNT": 10,
}
