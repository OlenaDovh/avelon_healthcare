"""Модуль `accounts/tokens.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations
from typing import Any

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Клас `EmailVerificationTokenGenerator` інкапсулює повʼязану логіку проєкту.

    Базові класи: `PasswordResetTokenGenerator`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    def _make_hash_value(self, user: Any, timestamp: Any) -> Any:
        """Виконує прикладну логіку функції `_make_hash_value` у відповідному модулі проєкту.

        Параметри:
            user: Значення типу `Any`, яке передається для виконання логіки функції.
            timestamp: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            Any: Результат роботи функції або обʼєкт, сформований під час виконання.
        """
        return f"{user.pk}{user.email}{user.pending_email}{user.email_verified}{timestamp}"


email_verification_token = EmailVerificationTokenGenerator()
