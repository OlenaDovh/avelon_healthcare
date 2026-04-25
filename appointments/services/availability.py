"""Модуль `appointments/services/availability.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations
from typing import Any

from datetime import date

from django.utils import timezone

from appointments.models import Appointment, AppointmentStatus


def get_available_slots_for_doctor_on_date(
    doctor,
    direction,
    target_date: date,
    exclude_appointment_id: int | None = None,
) -> list[dict[str, str]]:
    """Виконує прикладну логіку функції `get_available_slots_for_doctor_on_date` у відповідному модулі проєкту.

    Параметри:
        doctor: Значення типу `Any`, яке передається для виконання логіки функції.
        direction: Значення типу `Any`, яке передається для виконання логіки функції.
        target_date: Значення типу `date`, яке передається для виконання логіки функції.
        exclude_appointment_id: Значення типу `int | None`, яке передається для виконання логіки функції.

    Повертає:
        list[dict[str, str]]: Результат роботи функції або обʼєкт, сформований під час виконання.
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

    busy_times = set(busy_qs.values_list("appointment_time", flat=True))

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
    """Виконує прикладну логіку функції `get_available_dates_for_doctor_direction` у відповідному модулі проєкту.

    Параметри:
        doctor: Значення типу `Any`, яке передається для виконання логіки функції.
        direction: Значення типу `Any`, яке передається для виконання логіки функції.
        exclude_appointment_id: Значення типу `int | None`, яке передається для виконання логіки функції.

    Повертає:
        list[str]: Результат роботи функції або обʼєкт, сформований під час виконання.
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
