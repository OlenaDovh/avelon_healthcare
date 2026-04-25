"""Модуль appointments/services/creation.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
from django.db import transaction
from appointments.models import Appointment
from appointments.tasks import send_appointment_email_task

def fill_appointment_from_user(*, appointment: Appointment, user: Any) -> Appointment:
    """Виконує логіку `fill_appointment_from_user`.

Args:
    appointment: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    appointment.user = user
    appointment.last_name = user.last_name
    appointment.first_name = user.first_name
    appointment.middle_name = getattr(user, 'middle_name', '') or ''
    appointment.phone = getattr(user, 'phone', '') or ''
    appointment.email = user.email or ''
    return appointment

def fill_appointment_from_guest_data(*, appointment: Appointment, cleaned_data: dict) -> Appointment:
    """Виконує логіку `fill_appointment_from_guest_data`.

Args:
    appointment: Вхідне значення для виконання операції.
    cleaned_data: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    appointment.user = None
    appointment.last_name = cleaned_data['last_name']
    appointment.first_name = cleaned_data['first_name']
    appointment.middle_name = cleaned_data.get('middle_name', '')
    appointment.phone = cleaned_data['phone']
    appointment.email = cleaned_data['email']
    return appointment

def save_new_appointment(*, appointment: Appointment) -> Appointment:
    """Виконує логіку `save_new_appointment`.

Args:
    appointment: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    appointment.save()
    transaction.on_commit(lambda: send_appointment_email_task.delay(appointment.id))
    return appointment
