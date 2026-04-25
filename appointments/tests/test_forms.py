from __future__ import annotations

import pytest
from django.utils import timezone
from datetime import timedelta

from appointments.forms import (
    AppointmentCreateForm,
    GuestAppointmentCreateForm,
    SupportAppointmentCreateForm,
    SupportAppointmentUpdateForm,
)
from appointments.models import AppointmentStatus


def get_appointment_create_data(direction, doctor, **overrides) -> dict:
    """
    Формує дані для створення запису на прийом.

    Returns:
        dict: Дані форми.
    """
    data: dict = {
        "direction": direction.id,
        "doctor": doctor.id,
        "appointment_date": (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "appointment_time": "10:00",
        "description": "Первинна консультація",
    }
    data.update(overrides)
    return data


def get_guest_appointment_data(direction, doctor, **overrides) -> dict:
    """
    Формує дані для гостьового запису.

    Returns:
        dict: Дані форми.
    """
    data: dict = {
        "last_name": "Гість",
        "first_name": "Іван",
        "middle_name": "",
        "phone": "+380991111111",
        "email": "guest@example.com",
        **get_appointment_create_data(direction, doctor),
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_appointment_create_form_valid(direction, doctor, monkeypatch) -> None:
    """
    Перевіряє валідність форми створення запису.
    """
    target_date: str = (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d")

    monkeypatch.setattr(
        "appointments.forms.create.get_available_dates_for_doctor_direction",
        lambda doctor, direction: [target_date],
    )
    monkeypatch.setattr(
        "appointments.forms.create.get_available_slots_for_doctor_on_date",
        lambda doctor, direction, target_date: [
            {"value": "10:00", "label": "10:00 - 10:30"}
        ],
    )

    doctor.directions.add(direction)
    form: AppointmentCreateForm = AppointmentCreateForm(
        data=get_appointment_create_data(direction, doctor)
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_guest_appointment_create_form_valid(direction, doctor, monkeypatch) -> None:
    """
    Перевіряє валідність гостьової форми запису.
    """
    target_date: str = (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d")

    monkeypatch.setattr(
        "appointments.forms.create.get_available_dates_for_doctor_direction",
        lambda doctor, direction: [target_date],
    )
    monkeypatch.setattr(
        "appointments.forms.create.get_available_slots_for_doctor_on_date",
        lambda doctor, direction, target_date: [
            {"value": "10:00", "label": "10:00 - 10:30"}
        ],
    )

    doctor.directions.add(direction)
    form: GuestAppointmentCreateForm = GuestAppointmentCreateForm(
        data=get_guest_appointment_data(direction, doctor)
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_support_appointment_create_form_valid_for_registered_user(
    user, direction, doctor, monkeypatch
) -> None:
    """
    Перевіряє форму створення запису для зареєстрованого користувача.
    """
    target_date: str = (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d")

    monkeypatch.setattr(
        "appointments.forms.create.get_available_dates_for_doctor_direction",
        lambda doctor, direction: [target_date],
    )
    monkeypatch.setattr(
        "appointments.forms.create.get_available_slots_for_doctor_on_date",
        lambda doctor, direction, target_date: [
            {"value": "10:00", "label": "10:00 - 10:30"}
        ],
    )

    doctor.directions.add(direction)

    form: SupportAppointmentCreateForm = SupportAppointmentCreateForm(
        data={
            "user": user.id,
            "last_name": "",
            "first_name": "",
            "middle_name": "",
            "phone": "",
            "email": "",
            **get_appointment_create_data(direction, doctor),
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_support_appointment_create_form_valid_for_guest(direction, doctor, monkeypatch) -> None:
    """
    Перевіряє форму створення запису для гостя.
    """
    target_date: str = (timezone.localdate() + timedelta(days=1)).strftime("%Y-%m-%d")

    monkeypatch.setattr(
        "appointments.forms.create.get_available_dates_for_doctor_direction",
        lambda doctor, direction: [target_date],
    )
    monkeypatch.setattr(
        "appointments.forms.create.get_available_slots_for_doctor_on_date",
        lambda doctor, direction, target_date: [
            {"value": "10:00", "label": "10:00 - 10:30"}
        ],
    )

    doctor.directions.add(direction)

    form: SupportAppointmentCreateForm = SupportAppointmentCreateForm(
        data={
            "user": "",
            "last_name": "Гість",
            "first_name": "Іван",
            "middle_name": "",
            "phone": "+380991111112",
            "email": "guest2@example.com",
            **get_appointment_create_data(direction, doctor),
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_support_appointment_update_form_valid(appointment, monkeypatch) -> None:
    """
    Перевіряє валідність форми оновлення запису.
    """
    date_str: str = appointment.appointment_date.strftime("%Y-%m-%d")

    monkeypatch.setattr(
        "appointments.forms.update.get_available_dates_for_doctor_direction",
        lambda doctor, direction, exclude_appointment_id=None: [date_str],
    )
    monkeypatch.setattr(
        "appointments.forms.update.get_available_slots_for_doctor_on_date",
        lambda doctor, direction, appointment_date, exclude_appointment_id=None: [
            {"value": "10:00", "label": "10:00 - 10:30"}
        ],
    )

    appointment.doctor.directions.add(appointment.direction)

    form: SupportAppointmentUpdateForm = SupportAppointmentUpdateForm(
        instance=appointment,
        data={
            "direction": appointment.direction.id,
            "doctor": appointment.doctor.id,
            "appointment_date": date_str,
            "appointment_time": "10:00",
            "description": appointment.description,
            "status": AppointmentStatus.PLANNED,
            "rejection_reason": "",
        },
    )

    assert form.is_valid()