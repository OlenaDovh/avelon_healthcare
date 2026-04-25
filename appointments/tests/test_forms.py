"""Модуль appointments/tests/test_forms.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest
from datetime import timedelta
from django.utils import timezone
from appointments.forms import AppointmentCreateForm, GuestAppointmentCreateForm, SupportAppointmentCreateForm, SupportAppointmentUpdateForm
from appointments.models import AppointmentStatus

def get_appointment_create_data(direction: Any, doctor: Any, **overrides: Any) -> Any:
    """Виконує логіку `get_appointment_create_data`.

Args:
    direction: Вхідне значення для виконання операції.
    doctor: Вхідне значення для виконання операції.
    overrides: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    data = {'direction': direction.id, 'doctor': doctor.id, 'appointment_date': (timezone.localdate() + timedelta(days=1)).strftime('%Y-%m-%d'), 'appointment_time': '10:00', 'description': 'Первинна консультація'}
    data.update(overrides)
    return data

def get_guest_appointment_data(direction: Any, doctor: Any, **overrides: Any) -> Any:
    """Виконує логіку `get_guest_appointment_data`.

Args:
    direction: Вхідне значення для виконання операції.
    doctor: Вхідне значення для виконання операції.
    overrides: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    data = {'last_name': 'Гість', 'first_name': 'Іван', 'middle_name': '', 'phone': '+380991111111', 'email': 'guest@example.com', **get_appointment_create_data(direction, doctor)}
    data.update(overrides)
    return data

@pytest.mark.django_db
def test_appointment_create_form_valid(direction: Any, doctor: Any, monkeypatch: Any) -> None:
    """Виконує логіку `test_appointment_create_form_valid`.

Args:
    direction: Вхідне значення для виконання операції.
    doctor: Вхідне значення для виконання операції.
    monkeypatch: Вхідне значення для виконання операції.

Returns:
    None."""
    target_date = (timezone.localdate() + timedelta(days=1)).strftime('%Y-%m-%d')
    monkeypatch.setattr('appointments.forms.create.get_available_dates_for_doctor_direction', lambda doctor, direction: [target_date])
    monkeypatch.setattr('appointments.forms.create.get_available_slots_for_doctor_on_date', lambda doctor, direction, target_date: [{'value': '10:00', 'label': '10:00 - 10:30'}])
    doctor.directions.add(direction)
    form = AppointmentCreateForm(data=get_appointment_create_data(direction, doctor))
    assert form.is_valid()

@pytest.mark.django_db
def test_guest_appointment_create_form_valid(direction: Any, doctor: Any, monkeypatch: Any) -> None:
    """Виконує логіку `test_guest_appointment_create_form_valid`.

Args:
    direction: Вхідне значення для виконання операції.
    doctor: Вхідне значення для виконання операції.
    monkeypatch: Вхідне значення для виконання операції.

Returns:
    None."""
    target_date = (timezone.localdate() + timedelta(days=1)).strftime('%Y-%m-%d')
    monkeypatch.setattr('appointments.forms.create.get_available_dates_for_doctor_direction', lambda doctor, direction: [target_date])
    monkeypatch.setattr('appointments.forms.create.get_available_slots_for_doctor_on_date', lambda doctor, direction, target_date: [{'value': '10:00', 'label': '10:00 - 10:30'}])
    doctor.directions.add(direction)
    form = GuestAppointmentCreateForm(data=get_guest_appointment_data(direction, doctor))
    assert form.is_valid()

@pytest.mark.django_db
def test_support_appointment_create_form_valid_for_registered_user(user: Any, direction: Any, doctor: Any, monkeypatch: Any) -> None:
    """Виконує логіку `test_support_appointment_create_form_valid_for_registered_user`.

Args:
    user: Вхідне значення для виконання операції.
    direction: Вхідне значення для виконання операції.
    doctor: Вхідне значення для виконання операції.
    monkeypatch: Вхідне значення для виконання операції.

Returns:
    None."""
    target_date = (timezone.localdate() + timedelta(days=1)).strftime('%Y-%m-%d')
    monkeypatch.setattr('appointments.forms.create.get_available_dates_for_doctor_direction', lambda doctor, direction: [target_date])
    monkeypatch.setattr('appointments.forms.create.get_available_slots_for_doctor_on_date', lambda doctor, direction, target_date: [{'value': '10:00', 'label': '10:00 - 10:30'}])
    doctor.directions.add(direction)
    form = SupportAppointmentCreateForm(data={'user': user.id, 'last_name': '', 'first_name': '', 'middle_name': '', 'phone': '', 'email': '', **get_appointment_create_data(direction, doctor)})
    assert form.is_valid()

@pytest.mark.django_db
def test_support_appointment_create_form_valid_for_guest(direction: Any, doctor: Any, monkeypatch: Any) -> None:
    """Виконує логіку `test_support_appointment_create_form_valid_for_guest`.

Args:
    direction: Вхідне значення для виконання операції.
    doctor: Вхідне значення для виконання операції.
    monkeypatch: Вхідне значення для виконання операції.

Returns:
    None."""
    target_date = (timezone.localdate() + timedelta(days=1)).strftime('%Y-%m-%d')
    monkeypatch.setattr('appointments.forms.create.get_available_dates_for_doctor_direction', lambda doctor, direction: [target_date])
    monkeypatch.setattr('appointments.forms.create.get_available_slots_for_doctor_on_date', lambda doctor, direction, target_date: [{'value': '10:00', 'label': '10:00 - 10:30'}])
    doctor.directions.add(direction)
    form = SupportAppointmentCreateForm(data={'user': '', 'last_name': 'Гість', 'first_name': 'Іван', 'middle_name': '', 'phone': '+380991111112', 'email': 'guest2@example.com', **get_appointment_create_data(direction, doctor)})
    assert form.is_valid()

@pytest.mark.django_db
def test_support_appointment_update_form_valid(appointment: Any, monkeypatch: Any) -> None:
    """Виконує логіку `test_support_appointment_update_form_valid`.

Args:
    appointment: Вхідне значення для виконання операції.
    monkeypatch: Вхідне значення для виконання операції.

Returns:
    None."""
    date_str = appointment.appointment_date.strftime('%Y-%m-%d')
    monkeypatch.setattr('appointments.forms.update.get_available_dates_for_doctor_direction', lambda doctor, direction, exclude_appointment_id=None: [date_str])
    monkeypatch.setattr('appointments.forms.update.get_available_slots_for_doctor_on_date', lambda doctor, direction, appointment_date, exclude_appointment_id=None: [{'value': '10:00', 'label': '10:00 - 10:30'}])
    appointment.doctor.directions.add(appointment.direction)
    form = SupportAppointmentUpdateForm(instance=appointment, data={'direction': appointment.direction.id, 'doctor': appointment.doctor.id, 'appointment_date': date_str, 'appointment_time': '10:00', 'description': appointment.description, 'status': AppointmentStatus.PLANNED, 'rejection_reason': ''})
    assert form.is_valid()
