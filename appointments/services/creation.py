from __future__ import annotations

from appointments.models import Appointment
from appointments.services.notifications import send_appointment_email


def fill_appointment_from_user(*, appointment: Appointment, user) -> Appointment:
    appointment.user = user
    appointment.last_name = user.last_name
    appointment.first_name = user.first_name
    appointment.middle_name = getattr(user, "middle_name", "") or ""
    appointment.phone = getattr(user, "phone", "") or ""
    appointment.email = user.email or ""
    return appointment


def fill_appointment_from_guest_data(*, appointment: Appointment, cleaned_data: dict) -> Appointment:
    appointment.user = None
    appointment.last_name = cleaned_data["last_name"]
    appointment.first_name = cleaned_data["first_name"]
    appointment.middle_name = cleaned_data.get("middle_name", "")
    appointment.phone = cleaned_data["phone"]
    appointment.email = cleaned_data["email"]
    return appointment


def save_new_appointment(*, appointment: Appointment) -> Appointment:
    appointment.save()
    send_appointment_email(appointment)
    return appointment