"""Модуль appointments/tests/test_services.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest
from unittest.mock import patch
from datetime import time
from appointments.services import fill_appointment_from_guest_data, fill_appointment_from_user, save_new_appointment

@pytest.mark.django_db
def test_fill_appointment_from_user(appointment: Any, user: Any) -> None:
    """Виконує логіку `test_fill_appointment_from_user`.

Args:
    appointment: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.

Returns:
    None."""
    result = fill_appointment_from_user(appointment=appointment, user=user)
    assert result.user == user
    assert result.last_name == user.last_name
    assert result.first_name == user.first_name
    assert result.phone == user.phone
    assert result.email == user.email

@pytest.mark.django_db
def test_fill_appointment_from_guest_data(appointment: Any) -> None:
    """Виконує логіку `test_fill_appointment_from_guest_data`.

Args:
    appointment: Вхідне значення для виконання операції.

Returns:
    None."""
    cleaned_data = {'last_name': 'Гість', 'first_name': 'Іван', 'middle_name': 'Іванович', 'phone': '+380991111111', 'email': 'guest@example.com'}
    result = fill_appointment_from_guest_data(appointment=appointment, cleaned_data=cleaned_data)
    assert result.user is None
    assert result.last_name == 'Гість'
    assert result.first_name == 'Іван'
    assert result.phone == '+380991111111'
    assert result.email == 'guest@example.com'

@pytest.mark.django_db
@patch('appointments.services.creation.send_appointment_email')
def test_save_new_appointment_saves_and_sends_email(mock_send_appointment_email: Any, appointment: Any) -> None:
    """Виконує логіку `test_save_new_appointment_saves_and_sends_email`.

Args:
    mock_send_appointment_email: Вхідне значення для виконання операції.
    appointment: Вхідне значення для виконання операції.

Returns:
    None."""
    appointment.id = None
    appointment.appointment_time = time(11, 0)
    saved = save_new_appointment(appointment=appointment)
    assert saved.id is not None
    mock_send_appointment_email.assert_called_once_with(saved)
