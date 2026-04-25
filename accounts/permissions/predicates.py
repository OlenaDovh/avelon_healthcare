"""Модуль `accounts/permissions/predicates.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from typing import Any

from accounts.constants import (
    CONTENT_MANAGER_GROUP,
    DOCTOR_GROUP,
    HEAD_MANAGER_GROUP,
    PATIENT_GROUP,
    SUPPORT_GROUP,
)


def has_group(user: Any, group_name: str) -> bool:
    """Виконує прикладну логіку функції `has_group` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        group_name: Значення типу `str`, яке передається для виконання логіки функції.

    Повертає:
        bool: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return bool(
        getattr(user, "is_authenticated", False)
        and user.groups.filter(name=group_name).exists()
    )


def is_patient(user: Any) -> bool:
    """Виконує прикладну логіку функції `is_patient` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        bool: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return has_group(user, PATIENT_GROUP)


def is_support(user: Any) -> bool:
    """Виконує прикладну логіку функції `is_support` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        bool: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return has_group(user, SUPPORT_GROUP)


def is_doctor(user: Any) -> bool:
    """Виконує прикладну логіку функції `is_doctor` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        bool: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return has_group(user, DOCTOR_GROUP)


def is_head_manager(user: Any) -> bool:
    """Виконує прикладну логіку функції `is_head_manager` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        bool: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return has_group(user, HEAD_MANAGER_GROUP)


def is_content_manager(user: Any) -> bool:
    """Виконує прикладну логіку функції `is_content_manager` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        bool: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return has_group(user, CONTENT_MANAGER_GROUP)


def is_staff_role(user: Any) -> bool:
    """Виконує прикладну логіку функції `is_staff_role` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        bool: Результат роботи функції або обʼєкт, сформований під час виконання.
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
