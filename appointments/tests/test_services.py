"""Модуль `appointments/tests/test_services.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest
from unittest.mock import patch
from datetime import time

from appointments.services import (
    fill_appointment_from_guest_data,
    fill_appointment_from_user,
    save_new_appointment,
)


@pytest.mark.django_db
def test_fill_appointment_from_user(appointment: Any, user: Any) -> None:
    """Виконує прикладну логіку функції `test_fill_appointment_from_user` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    result = fill_appointment_from_user(appointment=appointment, user=user)

    assert result.user == user
    assert result.last_name == user.last_name
    assert result.first_name == user.first_name
    assert result.phone == user.phone
    assert result.email == user.email


@pytest.mark.django_db
def test_fill_appointment_from_guest_data(appointment: Any) -> None:
    """Виконує прикладну логіку функції `test_fill_appointment_from_guest_data` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    cleaned_data = {
        "last_name": "Гість",
        "first_name": "Іван",
        "middle_name": "Іванович",
        "phone": "+380991111111",
        "email": "guest@example.com",
    }

    result = fill_appointment_from_guest_data(
        appointment=appointment,
        cleaned_data=cleaned_data,
    )

    assert result.user is None
    assert result.last_name == "Гість"
    assert result.first_name == "Іван"
    assert result.phone == "+380991111111"
    assert result.email == "guest@example.com"


@pytest.mark.django_db
@patch("appointments.services.creation.send_appointment_email")
def test_save_new_appointment_saves_and_sends_email(
    mock_send_appointment_email,
    appointment,
):
    """Виконує прикладну логіку функції `test_save_new_appointment_saves_and_sends_email` у відповідному модулі проєкту.

    Параметри:
        mock_send_appointment_email: Значення типу `Any`, яке передається для виконання логіки функції.
        appointment: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    appointment.id = None
    appointment.appointment_time = time(11, 0)

    saved = save_new_appointment(appointment=appointment)

    assert saved.id is not None
    mock_send_appointment_email.assert_called_once_with(saved)
