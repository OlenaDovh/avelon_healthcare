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
    return bool(
        getattr(user, "is_authenticated", False)
        and user.groups.filter(name=group_name).exists()
    )


def is_patient(user: Any) -> bool:
    return has_group(user, PATIENT_GROUP)


def is_support(user: Any) -> bool:
    return has_group(user, SUPPORT_GROUP)


def is_doctor(user: Any) -> bool:
    return has_group(user, DOCTOR_GROUP)


def is_head_manager(user: Any) -> bool:
    return has_group(user, HEAD_MANAGER_GROUP)


def is_content_manager(user: Any) -> bool:
    return has_group(user, CONTENT_MANAGER_GROUP)


def is_staff_role(user: Any) -> bool:
    return any(
        (
            is_support(user),
            is_doctor(user),
            is_head_manager(user),
            is_content_manager(user),
            getattr(user, "is_superuser", False),
        )
    )