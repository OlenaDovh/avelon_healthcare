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
        @wraps(view_func)
        def wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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