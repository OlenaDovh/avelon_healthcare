from __future__ import annotations

import pytest
from django.contrib.auth.models import Group

from accounts.constants import (
    PATIENT_GROUP,
    SUPPORT_GROUP,
    DOCTOR_GROUP,
)


def get_group(name: str) -> Group:
    """
    Повертає або створює групу користувачів.

    Args:
        name: Назва групи.

    Returns:
        Group: Об'єкт групи.
    """
    return Group.objects.get_or_create(name=name)[0]


@pytest.mark.django_db
def test_new_user_added_to_patient_group(user_factory) -> None:
    """
    Перевіряє, що новий користувач додається до групи PATIENT.
    """
    user = user_factory()

    assert user.groups.filter(name=PATIENT_GROUP).exists()


@pytest.mark.django_db
@pytest.mark.parametrize("group_name", [SUPPORT_GROUP, DOCTOR_GROUP])
def test_user_becomes_staff_when_added_to_staff_groups(user_factory, group_name: str) -> None:
    """
    Перевіряє, що користувач стає staff при додаванні до staff-груп.
    """
    group = get_group(group_name)

    user = user_factory(is_staff=False)
    user.groups.add(group)
    user.refresh_from_db()

    assert user.is_staff is True