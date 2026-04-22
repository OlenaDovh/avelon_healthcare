from __future__ import annotations

from celery import shared_task
from django.template.loader import render_to_string

from core.utils.email import send_html_email
from appointments.models import Appointment


@shared_task
def send_appointment_email_task(appointment_id: int) -> None:
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return

    if not appointment.email:
        return

    html_body = render_to_string(
        "avelon_healthcare/appointments/email/appointment_email.html",
        {
            "appointment": appointment,
        },
    )

    send_html_email(
        subject=f"Avelon Healthcare — запис до лікаря #{appointment.id}",
        html_body=html_body,
        to=[appointment.email],
    )