"""Модуль accounts/tests/test_signals.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest
from django.contrib.auth.models import Group
from accounts.constants import PATIENT_GROUP, SUPPORT_GROUP, DOCTOR_GROUP

def get_group(name: Any) -> Any:
    """Виконує логіку `get_group`.

Args:
    name: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    return Group.objects.get_or_create(name=name)[0]

@pytest.mark.django_db
def test_new_user_added_to_patient_group(user_factory: Any) -> None:
    """Виконує логіку `test_new_user_added_to_patient_group`.

Args:
    user_factory: Вхідне значення для виконання операції.

Returns:
    None."""
    user = user_factory()
    assert user.groups.filter(name=PATIENT_GROUP).exists()

@pytest.mark.django_db
@pytest.mark.parametrize('group_name', [SUPPORT_GROUP, DOCTOR_GROUP])
def test_user_becomes_staff_when_added_to_staff_groups(user_factory: Any, group_name: Any) -> None:
    """Виконує логіку `test_user_becomes_staff_when_added_to_staff_groups`.

Args:
    user_factory: Вхідне значення для виконання операції.
    group_name: Вхідне значення для виконання операції.

Returns:
    None."""
    group = get_group(group_name)
    user = user_factory(is_staff=False)
    user.groups.add(group)
    user.refresh_from_db()
    assert user.is_staff is True
