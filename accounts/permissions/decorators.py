"""Модуль `accounts/permissions/decorators.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse

from .predicates import (
    is_content_manager,
    is_doctor,
    is_head_manager,
    is_support,
)


def role_required(predicate: Callable[[Any], bool]) -> Callable:
    """
    Універсальний декоратор для перевірки ролі користувача.
    """

    def decorator(view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
        """Виконує прикладну логіку функції `decorator` у відповідному модулі проєкту.

        Параметри:
            view_func: Значення типу `Callable[..., HttpResponse]`, яке передається для виконання логіки функції.

        Повертає:
            Callable[..., HttpResponse]: Результат роботи функції або обʼєкт, сформований під час виконання.
        """
        @wraps(view_func)
        def wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            """Виконує прикладну логіку функції `wrapped` у відповідному модулі проєкту.

            Параметри:
                request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
                *args: Значення типу `Any`, яке передається для виконання логіки функції.
                **kwargs: Значення типу `Any`, яке передається для виконання логіки функції.

            Повертає:
                HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
            """
            user = request.user

            if user.is_superuser or predicate(user):
                return view_func(request, *args, **kwargs)

            raise PermissionDenied

        return wrapped

    return decorator


support_required = role_required(is_support)
doctor_required = role_required(is_doctor)
content_manager_required = role_required(is_content_manager)
head_manager_required = role_required(is_head_manager)
