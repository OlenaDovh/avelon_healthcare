from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .constants import CONTENT_MANAGER_GROUP, HEAD_MANAGER_GROUP, PATIENT_GROUP

User = get_user_model()


@receiver(post_save, sender=User)
def add_user_to_patient_group(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs: object,
) -> None:
    """
    Додає нового користувача в групу patient.

    Args:
        sender (type[User]): Модель користувача.
        instance (User): Екземпляр користувача.
        created (bool): Ознака створення.
        **kwargs (object): Додаткові параметри.

    Returns:
        None
    """
    if not created:
        return

    group, _ = Group.objects.get_or_create(name=PATIENT_GROUP)
    instance.groups.add(group)


@receiver(m2m_changed, sender=User.groups.through)
def sync_staff_status_by_groups(
    sender: type[object],
    instance: User,
    action: str,
    **kwargs: object,
) -> None:
    """
    Синхронізує is_staff залежно від груп користувача.

    Args:
        sender (type[object]): Джерело сигналу.
        instance (User): Екземпляр користувача.
        action (str): Тип дії сигналу.
        **kwargs (object): Додаткові параметри.

    Returns:
        None
    """
    if action not in {"post_add", "post_remove", "post_clear"}:
        return

    if instance.is_superuser:
        return

    group_names: set[str] = set(instance.groups.values_list("name", flat=True))
    should_be_staff: bool = bool(
        {CONTENT_MANAGER_GROUP} & group_names
    )

    if instance.is_staff != should_be_staff:
        instance.is_staff = should_be_staff
        instance.save(update_fields=["is_staff"])