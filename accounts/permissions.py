from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from .constants import (
    CONTENT_MANAGER_GROUP,
    HEAD_MANAGER_GROUP,
    PATIENT_GROUP,
    SUPPORT_GROUP, DOCTOR_GROUP,
)


def has_group(user: Any, group_name: str) -> bool:
    """
    Перевіряє, чи входить користувач до вказаної групи.

    Args:
        user (Any): Користувач.
        group_name (str): Назва групи.

    Returns:
        bool: True, якщо користувач у групі.
    """
    return bool(
        getattr(user, "is_authenticated", False)
        and user.groups.filter(name=group_name).exists()
    )


def is_patient(user: Any) -> bool:
    """
    Перевіряє, чи є користувач пацієнтом.

    Args:
        user (Any): Користувач.

    Returns:
        bool: True, якщо користувач пацієнт.
    """
    return has_group(user, PATIENT_GROUP)


def is_support(user: Any) -> bool:
    """
    Перевіряє, чи є користувач support.

    Args:
        user (Any): Користувач.

    Returns:
        bool: True, якщо користувач support.
    """
    return has_group(user, SUPPORT_GROUP)


def is_head_manager(user: Any) -> bool:
    """
    Перевіряє, чи є користувач head manager.

    Args:
        user (Any): Користувач.

    Returns:
        bool: True, якщо користувач head manager.
    """
    return has_group(user, HEAD_MANAGER_GROUP)


def is_content_manager(user: Any) -> bool:
    """
    Перевіряє, чи є користувач content manager.

    Args:
        user (Any): Користувач.

    Returns:
        bool: True, якщо користувач content manager.
    """
    return has_group(user, CONTENT_MANAGER_GROUP)


def is_staff_role(user: Any) -> bool:
    """
    Перевіряє, чи є користувач однією з робочих ролей.

    Args:
        user (Any): Користувач.

    Returns:
        bool: True, якщо користувач staff role.
    """
    return any(
        (
            is_support(user),
            is_head_manager(user),
            is_content_manager(user),
            is_doctor(user),
            getattr(user, "is_superuser", False),
        )
    )


def support_required(
    view_func: Callable[..., HttpResponse],
) -> Callable[..., HttpResponse]:
    """
    Дозволяє доступ тільки support або superadmin.

    Args:
        view_func (Callable[..., HttpResponse]): View-функція.

    Returns:
        Callable[..., HttpResponse]: Обгорнута view-функція.
    """
    @wraps(view_func)
    def wrapped(
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        if request.user.is_superuser or is_support(request.user):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied

    return wrapped


def head_manager_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect("accounts:login")

        if user.is_superuser or user.groups.filter(name="head_manager").exists():
            return view_func(request, *args, **kwargs)

        messages.error(request, "У вас немає доступу до цієї сторінки.")
        return redirect("core:home")

    return wrapped


def content_manager_required(
    view_func: Callable[..., HttpResponse],
) -> Callable[..., HttpResponse]:
    """
    Дозволяє доступ тільки content manager або superadmin.

    Args:
        view_func (Callable[..., HttpResponse]): View-функція.

    Returns:
        Callable[..., HttpResponse]: Обгорнута view-функція.
    """
    @wraps(view_func)
    def wrapped(
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        if request.user.is_superuser or is_content_manager(request.user):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied

    return wrapped

def is_doctor(user: Any) -> bool:
    """
    Перевіряє, чи є користувач лікарем.

    Args:
        user (Any): Користувач.

    Returns:
        bool: True, якщо користувач лікар.
    """
    return has_group(user, DOCTOR_GROUP)

def doctor_required(
    view_func: Callable[..., HttpResponse],
) -> Callable[..., HttpResponse]:
    """
    Дозволяє доступ тільки doctor або superadmin.

    Args:
        view_func (Callable[..., HttpResponse]): View-функція.

    Returns:
        Callable[..., HttpResponse]: Обгорнута view-функція.
    """
    @wraps(view_func)
    def wrapped(
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        if request.user.is_superuser or is_doctor(request.user):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied

    return wrapped