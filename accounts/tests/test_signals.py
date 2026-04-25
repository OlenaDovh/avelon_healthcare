from typing import Any
import pytest
from django.contrib.auth.models import Group
from accounts.constants import PATIENT_GROUP, SUPPORT_GROUP, DOCTOR_GROUP

def get_group(name: Any) -> Any:
    """Виконує логіку `get_group`.

Args:
    name: Вхідний параметр `name`.

Returns:
    Any: Результат виконання."""
    return Group.objects.get_or_create(name=name)[0]

@pytest.mark.django_db
def test_new_user_added_to_patient_group(user_factory: Any) -> None:
    """Виконує логіку `test_new_user_added_to_patient_group`.

Args:
    user_factory: Вхідний параметр `user_factory`.

Returns:
    Any: Результат виконання."""
    user = user_factory()
    assert user.groups.filter(name=PATIENT_GROUP).exists()

@pytest.mark.django_db
@pytest.mark.parametrize('group_name', [SUPPORT_GROUP, DOCTOR_GROUP])
def test_user_becomes_staff_when_added_to_staff_groups(user_factory: Any, group_name: Any) -> None:
    """Виконує логіку `test_user_becomes_staff_when_added_to_staff_groups`.

Args:
    user_factory: Вхідний параметр `user_factory`.
    group_name: Вхідний параметр `group_name`.

Returns:
    Any: Результат виконання."""
    group = get_group(group_name)
    user = user_factory(is_staff=False)
    user.groups.add(group)
    user.refresh_from_db()
    assert user.is_staff is True
