"""Модуль appointments/tests/test_views.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from accounts.constants import SUPPORT_GROUP
from appointments.models import AppointmentStatus

def make_support(user: Any) -> Any:
    """Виконує логіку `make_support`.

Args:
    user: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    group, _ = Group.objects.get_or_create(name=SUPPORT_GROUP)
    user.groups.add(group)
    return user

@pytest.mark.django_db
def test_appointment_list_view_opens_for_logged_user(auth_client: Any) -> None:
    """Виконує логіку `test_appointment_list_view_opens_for_logged_user`.

Args:
    auth_client: Вхідне значення для виконання операції.

Returns:
    None."""
    response = auth_client.get(reverse('appointments:appointment_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_appointment_detail_view_opens_for_owner(client: Any, user: Any, appointment: Any) -> None:
    """Виконує логіку `test_appointment_detail_view_opens_for_owner`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.
    appointment: Вхідне значення для виконання операції.

Returns:
    None."""
    appointment.user = user
    appointment.save()
    client.force_login(user)
    response = client.get(reverse('appointments:appointment_detail', args=[appointment.id]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_appointment_cancel_view_changes_status_to_rejected(client: Any, user: Any, appointment: Any) -> None:
    """Виконує логіку `test_appointment_cancel_view_changes_status_to_rejected`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.
    appointment: Вхідне значення для виконання операції.

Returns:
    None."""
    appointment.user = user
    appointment.status = AppointmentStatus.PLANNED
    appointment.save()
    client.force_login(user)
    response = client.get(reverse('appointments:appointment_cancel', args=[appointment.id]))
    assert response.status_code in (302, 301)
    appointment.refresh_from_db()
    assert appointment.status == AppointmentStatus.REJECTED

@pytest.mark.django_db
def test_support_appointment_list_view_opens_for_support(client: Any, user: Any) -> None:
    """Виконує логіку `test_support_appointment_list_view_opens_for_support`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.

Returns:
    None."""
    make_support(user)
    client.force_login(user)
    response = client.get(reverse('appointments:support_appointment_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_support_appointment_create_view_get_opens_for_support(client: Any, user: Any) -> None:
    """Виконує логіку `test_support_appointment_create_view_get_opens_for_support`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.

Returns:
    None."""
    make_support(user)
    client.force_login(user)
    response = client.get(reverse('appointments:support_appointment_create'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_support_appointment_update_view_get_opens_for_support(client: Any, user: Any, appointment: Any) -> None:
    """Виконує логіку `test_support_appointment_update_view_get_opens_for_support`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.
    appointment: Вхідне значення для виконання операції.

Returns:
    None."""
    make_support(user)
    client.force_login(user)
    response = client.get(reverse('appointments:support_appointment_update', args=[appointment.id]))
    assert response.status_code == 200
