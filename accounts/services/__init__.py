"""Модуль `accounts/services/__init__.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .email_verification import build_email_verification_url, send_verification_email
from .roles import assign_group_permissions, setup_roles
