from __future__ import annotations

from datetime import date

from django.template.loader import render_to_string
from django.utils import timezone

from .models import Appointment, AppointmentStatus
from core.utils.email import send_html_email


def get_available_slots_for_doctor_on_date(doctor, direction, target_date: date) -> list[dict[str, str]]:
    today = timezone.localdate()
    now_time = timezone.localtime().time()

    if target_date < today:
        return []

    workday = doctor.workdays.filter(
        work_date=target_date,
        direction=direction,
    ).prefetch_related("periods").first()

    if not workday:
        return []

    busy_times = set(
        Appointment.objects.filter(
            doctor=doctor,
            direction=direction,
            appointment_date=target_date,
            status=AppointmentStatus.PLANNED,
        ).values_list("appointment_time", flat=True)
    )

    slots = []

    for period in workday.periods.all():
        for slot_start, slot_end in period.get_slots():
            if target_date == today and slot_end.time() <= now_time:
                continue

            if slot_start.time() in busy_times:
                continue

            slots.append(
                {
                    "value": slot_start.strftime("%H:%M"),
                    "label": f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}",
                }
            )

    return slots

def send_appointment_email(appointment: Appointment) -> None:
    """
    Надсилає лист із даними запису до лікаря.

    Args:
        appointment (Appointment): Запис до лікаря.

    Returns:
        None
    """
    html_body: str = render_to_string(
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