"""Модуль appointments/tests/test_models.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest
from django.core.exceptions import ValidationError
from appointments.models import AppointmentStatus

@pytest.mark.django_db
def test_appointment_factory_creates_appointment(appointment: Any) -> None:
    """Виконує логіку `test_appointment_factory_creates_appointment`.

Args:
    appointment: Вхідне значення для виконання операції.

Returns:
    None."""
    assert appointment.id is not None
    assert appointment.status == AppointmentStatus.PLANNED

@pytest.mark.django_db
def test_appointment_full_name_property(appointment: Any) -> None:
    """Виконує логіку `test_appointment_full_name_property`.

Args:
    appointment: Вхідне значення для виконання операції.

Returns:
    None."""
    expected = ' '.join(filter(None, [appointment.last_name, appointment.first_name, appointment.middle_name]))
    assert appointment.full_name == expected

@pytest.mark.django_db
def test_appointment_customer_name_returns_full_name(appointment: Any) -> None:
    """Виконує логіку `test_appointment_customer_name_returns_full_name`.

Args:
    appointment: Вхідне значення для виконання операції.

Returns:
    None."""
    assert appointment.customer_name == appointment.full_name

@pytest.mark.django_db
def test_appointment_clean_raises_if_doctor_not_in_direction(appointment: Any, direction_factory: Any) -> None:
    """Виконує логіку `test_appointment_clean_raises_if_doctor_not_in_direction`.

Args:
    appointment: Вхідне значення для виконання операції.
    direction_factory: Вхідне значення для виконання операції.

Returns:
    None."""
    appointment.direction = direction_factory()
    with pytest.raises(ValidationError):
        appointment.clean()

@pytest.mark.django_db
def test_appointment_clean_requires_rejection_reason(appointment: Any) -> None:
    """Виконує логіку `test_appointment_clean_requires_rejection_reason`.

Args:
    appointment: Вхідне значення для виконання операції.

Returns:
    None."""
    appointment.status = AppointmentStatus.REJECTED
    appointment.rejection_reason = ''
    with pytest.raises(ValidationError):
        appointment.clean()
