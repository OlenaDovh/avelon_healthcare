from __future__ import annotations

from django.http import HttpRequest


def user_roles(request: HttpRequest) -> dict[str, bool]:
    user = request.user

    if not user.is_authenticated:
        return {
            "is_patient": False,
            "is_support": False,
            "is_doctor": False,
            "is_head_manager": False,
            "is_content_manager": False,
            "is_staff_role": False,
            "is_superadmin": False,
        }

    group_names: set[str] = set(user.groups.values_list("name", flat=True))

    is_support: bool = "support" in group_names
    is_doctor: bool = "doctor" in group_names
    is_head_manager: bool = "head_manager" in group_names
    is_content_manager: bool = "content_manager" in group_names
    is_superadmin: bool = user.is_superuser

    is_staff_role: bool = any(
        (
            is_support,
            is_doctor,
            is_head_manager,
            is_content_manager,
            is_superadmin,
        )
    )

    return {
        "is_patient": "patient" in group_names,
        "is_support": is_support,
        "is_doctor": is_doctor,
        "is_head_manager": is_head_manager,
        "is_content_manager": is_content_manager,
        "is_staff_role": is_staff_role,
        "is_superadmin": is_superadmin,
    }