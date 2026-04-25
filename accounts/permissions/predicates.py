from __future__ import annotations
from typing import Any
from accounts.constants import CONTENT_MANAGER_GROUP, DOCTOR_GROUP, HEAD_MANAGER_GROUP, PATIENT_GROUP, SUPPORT_GROUP

def has_group(user: Any, group_name: str) -> bool:
    """Виконує логіку `has_group`.

Args:
    user: Вхідний параметр `user`.
    group_name: Вхідний параметр `group_name`.

Returns:
    Any: Результат виконання."""
    return bool(getattr(user, 'is_authenticated', False) and user.groups.filter(name=group_name).exists())

def is_patient(user: Any) -> bool:
    """Виконує логіку `is_patient`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    return has_group(user, PATIENT_GROUP)

def is_support(user: Any) -> bool:
    """Виконує логіку `is_support`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    return has_group(user, SUPPORT_GROUP)

def is_doctor(user: Any) -> bool:
    """Виконує логіку `is_doctor`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    return has_group(user, DOCTOR_GROUP)

def is_head_manager(user: Any) -> bool:
    """Виконує логіку `is_head_manager`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    return has_group(user, HEAD_MANAGER_GROUP)

def is_content_manager(user: Any) -> bool:
    """Виконує логіку `is_content_manager`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    return has_group(user, CONTENT_MANAGER_GROUP)

def is_staff_role(user: Any) -> bool:
    """Виконує логіку `is_staff_role`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    return any((is_support(user), is_doctor(user), is_head_manager(user), is_content_manager(user), getattr(user, 'is_superuser', False)))
