"""Модуль `appointments/tests/test_views.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest
from django.contrib.auth.models import Group
from django.urls import reverse

from accounts.constants import SUPPORT_GROUP
from appointments.models import AppointmentStatus


def make_support(user: Any) -> Any:
    """Виконує прикладну логіку функції `make_support` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    group, _ = Group.objects.get_or_create(name=SUPPORT_GROUP)
    user.groups.add(group)
    return user


@pytest.mark.django_db
def test_appointment_list_view_opens_for_logged_user(auth_client: Any) -> None:
    """Виконує прикладну логіку функції `test_appointment_list_view_opens_for_logged_user` у відповідному модулі проєкту.

    Параметри:
        auth_client: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    response = auth_client.get(reverse("appointments:appointment_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_appointment_detail_view_opens_for_owner(client: Any, user: Any, appointment: Any) -> None:
    """Виконує прикладну логіку функції `test_appointment_detail_view_opens_for_owner` у відповідному модулі проєкту.

    Параметри:
        client: Значення типу `Any`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    appointment.user = user
    appointment.save()
    client.force_login(user)

    response = client.get(reverse("appointments:appointment_detail", args=[appointment.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_appointment_cancel_view_changes_status_to_rejected(client: Any, user: Any, appointment: Any) -> None:
    """Виконує прикладну логіку функції `test_appointment_cancel_view_changes_status_to_rejected` у відповідному модулі проєкту.

    Параметри:
        client: Значення типу `Any`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    appointment.user = user
    appointment.status = AppointmentStatus.PLANNED
    appointment.save()
    client.force_login(user)

    response = client.get(reverse("appointments:appointment_cancel", args=[appointment.id]))
    assert response.status_code in (302, 301)

    appointment.refresh_from_db()
    assert appointment.status == AppointmentStatus.REJECTED


@pytest.mark.django_db
def test_support_appointment_list_view_opens_for_support(client: Any, user: Any) -> None:
    """Виконує прикладну логіку функції `test_support_appointment_list_view_opens_for_support` у відповідному модулі проєкту.

    Параметри:
        client: Значення типу `Any`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    make_support(user)
    client.force_login(user)

    response = client.get(reverse("appointments:support_appointment_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_support_appointment_create_view_get_opens_for_support(client: Any, user: Any) -> None:
    """Виконує прикладну логіку функції `test_support_appointment_create_view_get_opens_for_support` у відповідному модулі проєкту.

    Параметри:
        client: Значення типу `Any`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    make_support(user)
    client.force_login(user)

    response = client.get(reverse("appointments:support_appointment_create"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_support_appointment_update_view_get_opens_for_support(client: Any, user: Any, appointment: Any) -> None:
    """Виконує прикладну логіку функції `test_support_appointment_update_view_get_opens_for_support` у відповідному модулі проєкту.

    Параметри:
        client: Значення типу `Any`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    make_support(user)
    client.force_login(user)

    response = client.get(reverse("appointments:support_appointment_update", args=[appointment.id]))
    assert response.status_code == 200
