import pytest
from django.contrib.auth.models import Group
from accounts.constants import CONTENT_MANAGER_GROUP, DOCTOR_GROUP, HEAD_MANAGER_GROUP, PATIENT_GROUP, SUPPORT_GROUP
from accounts.services import assign_group_permissions, setup_roles

@pytest.mark.django_db
def test_setup_roles_creates_all_groups() -> None:
    """Виконує логіку `test_setup_roles_creates_all_groups`.

Returns:
    Any: Результат виконання."""
    setup_roles()
    assert Group.objects.filter(name=PATIENT_GROUP).exists()
    assert Group.objects.filter(name=SUPPORT_GROUP).exists()
    assert Group.objects.filter(name=HEAD_MANAGER_GROUP).exists()
    assert Group.objects.filter(name=CONTENT_MANAGER_GROUP).exists()
    assert Group.objects.filter(name=DOCTOR_GROUP).exists()

@pytest.mark.django_db
def test_assign_group_permissions_assigns_some_permissions() -> None:
    """Виконує логіку `test_assign_group_permissions_assigns_some_permissions`.

Returns:
    Any: Результат виконання."""
    assign_group_permissions()
    support_group = Group.objects.get(name=SUPPORT_GROUP)
    head_manager_group = Group.objects.get(name=HEAD_MANAGER_GROUP)
    content_manager_group = Group.objects.get(name=CONTENT_MANAGER_GROUP)
    doctor_group = Group.objects.get(name=DOCTOR_GROUP)
    assert support_group.permissions.exists()
    assert head_manager_group.permissions.exists()
    assert content_manager_group.permissions.exists()
    assert doctor_group.permissions.exists()
