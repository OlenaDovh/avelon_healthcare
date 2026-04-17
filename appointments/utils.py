from __future__ import annotations

from datetime import date

from django.template.loader import render_to_string
from django.utils import timezone

from .models import Appointment, AppointmentStatus
from core.utils.email import send_html_email


def get_available_slots_for_doctor_on_date(
    doctor,
    direction,
    target_date: date,
    exclude_appointment_id: int | None = None,
) -> list[dict[str, str]]:
    """
    Повертає тільки доступні слоти для лікаря на конкретну дату.

    Правила:
    - минулі дати недоступні
    - для сьогоднішньої дати не показуються слоти, час початку яких уже настав або минув
    - слот вважається зайнятим, якщо існує будь-який запис, крім rejected
    - під час редагування можна виключити поточний запис з перевірки
    """
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

    busy_qs = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=target_date,
    ).exclude(
        status=AppointmentStatus.REJECTED,
    )

    if exclude_appointment_id:
        busy_qs = busy_qs.exclude(id=exclude_appointment_id)

    busy_times = set(
        busy_qs.values_list("appointment_time", flat=True)
    )

    slots: list[dict[str, str]] = []

    for period in workday.periods.all():
        for slot_start, slot_end in period.get_slots():
            if target_date == today and slot_start.time() <= now_time:
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


def get_available_dates_for_doctor_direction(
    doctor,
    direction,
    exclude_appointment_id: int | None = None,
) -> list[str]:
    """
    Повертає тільки ті дати, на які реально є хоча б один доступний слот.
    """
    today = timezone.localdate()

    workdays = doctor.workdays.filter(
        direction=direction,
        work_date__gte=today,
    ).prefetch_related("periods").order_by("work_date")

    result: list[str] = []

    for workday in workdays:
        slots = get_available_slots_for_doctor_on_date(
            doctor,
            direction,
            workday.work_date,
            exclude_appointment_id=exclude_appointment_id,
        )
        if slots:
            result.append(workday.work_date.strftime("%Y-%m-%d"))

    return result


def send_appointment_email(appointment: Appointment) -> None:
    """
    Надсилає лист із даними запису до лікаря.
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