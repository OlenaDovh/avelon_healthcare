"""Модуль `appointments/services/creation.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations
from typing import Any

from django.db import transaction

from appointments.models import Appointment
from appointments.tasks import send_appointment_email_task


def fill_appointment_from_user(*, appointment: Appointment, user: Any) -> Appointment:
    """Виконує прикладну логіку функції `fill_appointment_from_user` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Appointment`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Appointment: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    appointment.user = user
    appointment.last_name = user.last_name
    appointment.first_name = user.first_name
    appointment.middle_name = getattr(user, "middle_name", "") or ""
    appointment.phone = getattr(user, "phone", "") or ""
    appointment.email = user.email or ""
    return appointment


def fill_appointment_from_guest_data(*, appointment: Appointment, cleaned_data: dict) -> Appointment:
    """Виконує прикладну логіку функції `fill_appointment_from_guest_data` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Appointment`, яке передається для виконання логіки функції.
        cleaned_data: Значення типу `dict`, яке передається для виконання логіки функції.

    Повертає:
        Appointment: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    appointment.user = None
    appointment.last_name = cleaned_data["last_name"]
    appointment.first_name = cleaned_data["first_name"]
    appointment.middle_name = cleaned_data.get("middle_name", "")
    appointment.phone = cleaned_data["phone"]
    appointment.email = cleaned_data["email"]
    return appointment


def save_new_appointment(*, appointment: Appointment) -> Appointment:
    """Виконує прикладну логіку функції `save_new_appointment` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Appointment`, яке передається для виконання логіки функції.

    Повертає:
        Appointment: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    appointment.save()

    transaction.on_commit(
        lambda: send_appointment_email_task.delay(appointment.id)
    )

    return appointment
