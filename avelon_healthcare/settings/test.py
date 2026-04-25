"""Модуль `avelon_healthcare/settings/test.py` застосунку `avelon_healthcare`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}
