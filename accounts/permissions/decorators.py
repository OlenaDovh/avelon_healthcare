from __future__ import annotations
from functools import wraps
from typing import Any, Callable
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from .predicates import (
    is_content_manager,
    is_doctor,
    is_head_manager,
    is_support,
)


def role_required(predicate: Callable[[Any], bool]) -> Callable[..., Callable[..., HttpResponse]]:
    """
    Універсальний декоратор для перевірки ролі користувача.

    Args:
        predicate: Функція-предикат для перевірки ролі користувача.

    Returns:
        Callable[..., HttpResponse]: Декоратор для обмеження доступу до view.
    """

    def decorator(view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
        """
        Обгортає view-функцію перевіркою ролі користувача.

        Args:
            view_func: Функція представлення.

        Returns:
            Callable[..., HttpResponse]: Обгорнута функція представлення.
        """

        @wraps(view_func)
        def wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            """
            Перевіряє доступ користувача перед виконанням view.

            Args:
                request: HTTP-запит.
                *args: Позиційні аргументи.
                **kwargs: Іменовані аргументи.

            Returns:
                HttpResponse: Відповідь view-функції.

            Raises:
                PermissionDenied: Якщо користувач не має доступу.
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
