"""Модуль `appointments/tests/test_models.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest
from django.core.exceptions import ValidationError

from appointments.models import AppointmentStatus


@pytest.mark.django_db
def test_appointment_factory_creates_appointment(appointment: Any) -> None:
    """Виконує прикладну логіку функції `test_appointment_factory_creates_appointment` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    assert appointment.id is not None
    assert appointment.status == AppointmentStatus.PLANNED


@pytest.mark.django_db
def test_appointment_full_name_property(appointment: Any) -> None:
    """Виконує прикладну логіку функції `test_appointment_full_name_property` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    expected = " ".join(
        filter(None, [appointment.last_name, appointment.first_name, appointment.middle_name])
    )
    assert appointment.full_name == expected


@pytest.mark.django_db
def test_appointment_customer_name_returns_full_name(appointment: Any) -> None:
    """Виконує прикладну логіку функції `test_appointment_customer_name_returns_full_name` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    assert appointment.customer_name == appointment.full_name


@pytest.mark.django_db
def test_appointment_clean_raises_if_doctor_not_in_direction(appointment: Any, direction_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_appointment_clean_raises_if_doctor_not_in_direction` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.
        direction_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    appointment.direction = direction_factory()

    with pytest.raises(ValidationError):
        appointment.clean()


@pytest.mark.django_db
def test_appointment_clean_requires_rejection_reason(appointment: Any) -> None:
    """Виконує прикладну логіку функції `test_appointment_clean_requires_rejection_reason` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    appointment.status = AppointmentStatus.REJECTED
    appointment.rejection_reason = ""

    with pytest.raises(ValidationError):
        appointment.clean()
