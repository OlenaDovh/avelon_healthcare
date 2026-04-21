from __future__ import annotations

from django.contrib.auth.models import Group, Permission
from django.db.utils import IntegrityError

from .constants import (
    CONTENT_MANAGER_GROUP,
    HEAD_MANAGER_GROUP,
    PATIENT_GROUP,
    SUPPORT_GROUP, DOCTOR_GROUP,
)


def setup_roles() -> None:
    """
    Створює базові групи ролей.

    Returns:
        None
    """
    for group_name in (
        PATIENT_GROUP,
        SUPPORT_GROUP,
        HEAD_MANAGER_GROUP,
        CONTENT_MANAGER_GROUP,
        DOCTOR_GROUP,
    ):
        Group.objects.get_or_create(name=group_name)


def assign_group_permissions() -> None:
    """
    Призначає дозволи групам.

    Returns:
        None
    """
    setup_roles()

    support_group: Group = Group.objects.get(name=SUPPORT_GROUP)
    head_manager_group: Group = Group.objects.get(name=HEAD_MANAGER_GROUP)
    content_manager_group: Group = Group.objects.get(name=CONTENT_MANAGER_GROUP)
    doctor_group: Group = Group.objects.get(name=DOCTOR_GROUP)

    support_permissions: list[tuple[str, str]] = [
        ("accounts", "view_user"),
        ("accounts", "change_user"),
        ("appointments", "view_appointment"),
        ("appointments", "change_appointment"),
        ("appointments", "add_appointment"),
        ("orders", "view_order"),
        ("orders", "change_order"),
        ("orders", "add_order"),
        ("orders", "view_orderitem"),
        ("orders", "add_orderitem"),
        ("orders", "change_orderitem"),
    ]

    head_manager_permissions: list[tuple[str, str]] = [
        ("doctors", "view_doctor"),
        ("doctors", "add_doctor"),
        ("doctors", "change_doctor"),
        ("doctors", "view_direction"),
        ("doctors", "add_direction"),
        ("doctors", "change_direction"),
        ("doctors", "view_doctorworkday"),
        ("doctors", "add_doctorworkday"),
        ("doctors", "change_doctorworkday"),
        ("doctors", "view_doctorworkperiod"),
        ("doctors", "add_doctorworkperiod"),
        ("doctors", "change_doctorworkperiod"),
        ("analysis", "view_analysis"),
        ("analysis", "add_analysis"),
        ("analysis", "change_analysis"),
    ]

    content_manager_permissions: list[tuple[str, str]] = [
        ("core", "view_clinicinfo"),
        ("core", "change_clinicinfo"),
        ("core", "view_contactinfo"),
        ("core", "change_contactinfo"),
        ("core", "view_promotion"),
        ("core", "add_promotion"),
        ("core", "change_promotion"),
        ("reviews", "view_review"),
        ("reviews", "change_review"),
    ]

    doctor_permissions: list[tuple[str, str]] = [
        ("appointments", "view_appointment"),
        ("appointments", "change_appointment"),
        ("appointments", "add_appointment"),
        ("doctors", "view_doctorworkday"),
        ("doctors", "add_doctorworkday"),
        ("doctors", "change_doctorworkday"),
        ("doctors", "view_doctorworkperiod"),
        ("doctors", "add_doctorworkperiod"),
        ("doctors", "change_doctorworkperiod"),
    ]

    support_group.permissions.set(_get_permissions(support_permissions))
    head_manager_group.permissions.set(_get_permissions(head_manager_permissions))
    content_manager_group.permissions.set(_get_permissions(content_manager_permissions))
    doctor_group.permissions.set(_get_permissions(doctor_permissions))

def _get_permissions(items: list[tuple[str, str]]) -> list[Permission]:
    """
    Повертає список Permission за app_label і codename.

    Args:
        items (list[tuple[str, str]]): Список дозволів.

    Returns:
        list[Permission]: Список об'єктів Permission.
    """
    permissions: list[Permission] = []

    for app_label, codename in items:
        try:
            permissions.append(
                Permission.objects.get(
                    content_type__app_label=app_label,
                    codename=codename,
                )
            )
        except Permission.DoesNotExist:
            continue
        except IntegrityError:
            continue

    return permissions