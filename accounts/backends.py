"""Модуль `accounts/backends.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpRequest

UserModel = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """Клас `EmailOrUsernameBackend` інкапсулює повʼязану логіку проєкту.

    Базові класи: `ModelBackend`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> UserModel | None:
        """Виконує прикладну логіку функції `authenticate` у відповідному модулі проєкту.

        Параметри:
            request: Значення типу `HttpRequest | None`, яке передається для виконання логіки функції.
            username: Значення типу `str | None`, яке передається для виконання логіки функції.
            password: Значення типу `str | None`, яке передається для виконання логіки функції.
            **kwargs: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            UserModel | None: Результат роботи функції або обʼєкт, сформований під час виконання.
        """
        login_value: str | None = username or kwargs.get("email")

        if not login_value or not password:
            return None

        user = UserModel.objects.filter(
            Q(username__iexact=login_value) | Q(email__iexact=login_value)
        ).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
