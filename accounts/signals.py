from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from accounts.constants import (
    CONTENT_MANAGER_GROUP,
    DOCTOR_GROUP,
    HEAD_MANAGER_GROUP,
    PATIENT_GROUP,
    SUPPORT_GROUP,
)

User = get_user_model()

STAFF_GROUPS = {
    SUPPORT_GROUP,
    DOCTOR_GROUP,
    HEAD_MANAGER_GROUP,
    CONTENT_MANAGER_GROUP,
}


@receiver(post_save, sender=User)
def add_user_to_patient_group(sender, instance: User, created: bool, **kwargs) -> None:
    if not created:
        return

    group, _ = Group.objects.get_or_create(name=PATIENT_GROUP)
    instance.groups.add(group)


@receiver(m2m_changed, sender=User.groups.through)
def sync_staff_status_by_groups(sender, instance: User, action: str, **kwargs) -> None:
    if action not in {"post_add", "post_remove", "post_clear"}:
        return

    if instance.is_superuser:
        return

    group_names = set(instance.groups.values_list("name", flat=True))
    should_be_staff = bool(STAFF_GROUPS & group_names)

    if instance.is_staff != should_be_staff:
        instance.is_staff = should_be_staff
        instance.save(update_fields=["is_staff"])