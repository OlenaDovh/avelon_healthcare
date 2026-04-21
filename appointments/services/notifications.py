from __future__ import annotations

from django.template.loader import render_to_string

from core.utils.email import send_html_email
from appointments.models import Appointment


def send_appointment_email(appointment: Appointment) -> None:
    html_body = render_to_string(
        "avelon_healthcare/appointments/appointment_email.html",
        {
            "appointment": appointment,
        },
    )

    send_html_email(
        subject=f"Avelon Healthcare — запис до лікаря #{appointment.id}",
        html_body=html_body,
        to=[appointment.email],
    )