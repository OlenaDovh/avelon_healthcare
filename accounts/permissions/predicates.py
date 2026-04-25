from typing import Any
from accounts.constants import (
    CONTENT_MANAGER_GROUP,
    DOCTOR_GROUP,
    HEAD_MANAGER_GROUP,
    PATIENT_GROUP,
    SUPPORT_GROUP,
)


def has_group(user: Any, group_name: str) -> bool:
    """
    Перевіряє, чи належить користувач до заданої групи.

    Args:
        user: Об'єкт користувача.
        group_name: Назва групи.

    Returns:
        bool: True, якщо користувач входить до групи, інакше False.
    """
    return bool(
        getattr(user, "is_authenticated", False)
        and user.groups.filter(name=group_name).exists()
    )


def is_patient(user: Any) -> bool:
    """
    Перевіряє, чи є користувач пацієнтом.

    Args:
        user: Об'єкт користувача.

    Returns:
        bool: True, якщо користувач є пацієнтом.
    """
    return has_group(user, PATIENT_GROUP)


def is_support(user: Any) -> bool:
    """
    Перевіряє, чи є користувач support-спеціалістом.

    Args:
        user: Об'єкт користувача.

    Returns:
        bool: True, якщо користувач належить до support.
    """
    return has_group(user, SUPPORT_GROUP)


def is_doctor(user: Any) -> bool:
    """
    Перевіряє, чи є користувач лікарем.

    Args:
        user: Об'єкт користувача.

    Returns:
        bool: True, якщо користувач є лікарем.
    """
    return has_group(user, DOCTOR_GROUP)


def is_head_manager(user: Any) -> bool:
    """
    Перевіряє, чи є користувач головним менеджером.

    Args:
        user: Об'єкт користувача.

    Returns:
        bool: True, якщо користувач є головним менеджером.
    """
    return has_group(user, HEAD_MANAGER_GROUP)


def is_content_manager(user: Any) -> bool:
    """
    Перевіряє, чи є користувач контент-менеджером.

    Args:
        user: Об'єкт користувача.

    Returns:
        bool: True, якщо користувач є контент-менеджером.
    """
    return has_group(user, CONTENT_MANAGER_GROUP)


def is_staff_role(user: Any) -> bool:
    """
    Перевіряє, чи має користувач одну зі службових ролей.

    Args:
        user: Об'єкт користувача.

    Returns:
        bool: True, якщо користувач має будь-яку службову роль або є суперкористувачем.
    """
    return any(
        (
            is_support(user),
            is_doctor(user),
            is_head_manager(user),
            is_content_manager(user),
            getattr(user, "is_superuser", False),
        )
    )