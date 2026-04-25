"""Модуль `appointments/views/ajax.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from datetime import datetime

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET

from doctors.models import Direction, Doctor
from appointments.services import (
    get_available_dates_for_doctor_direction,
    get_available_slots_for_doctor_on_date,
)


@require_GET
def available_slots(request: HttpRequest) -> JsonResponse:
    """Виконує прикладну логіку функції `available_slots` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        JsonResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    doctor_id = request.GET.get("doctor_id")
    direction_id = request.GET.get("direction_id")
    appointment_date = request.GET.get("date")
    exclude_appointment_id = request.GET.get("exclude_appointment_id")

    if not doctor_id or not direction_id or not appointment_date:
        return JsonResponse({"slots": []})

    try:
        doctor = Doctor.objects.get(id=doctor_id)
        direction = Direction.objects.get(id=direction_id)
    except (Doctor.DoesNotExist, Direction.DoesNotExist):
        return JsonResponse({"slots": []})

    try:
        selected_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"slots": []})

    exclude_id = None
    if exclude_appointment_id:
        try:
            exclude_id = int(exclude_appointment_id)
        except ValueError:
            exclude_id = None

    slots = get_available_slots_for_doctor_on_date(
        doctor,
        direction,
        selected_date,
        exclude_appointment_id=exclude_id,
    )
    return JsonResponse({"slots": slots})


@require_GET
def available_doctors(request: HttpRequest) -> JsonResponse:
    """Виконує прикладну логіку функції `available_doctors` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        JsonResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    direction_id = request.GET.get("direction_id")

    if not direction_id:
        return JsonResponse({"doctors": []})

    doctors = Doctor.objects.filter(
        directions__id=direction_id
    ).distinct().order_by("last_name", "first_name")

    return JsonResponse(
        {
            "doctors": [
                {
                    "id": doctor.id,
                    "full_name": doctor.full_name,
                }
                for doctor in doctors
            ]
        }
    )


@require_GET
def available_dates(request: HttpRequest) -> JsonResponse:
    """Виконує прикладну логіку функції `available_dates` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        JsonResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    doctor_id = request.GET.get("doctor_id")
    direction_id = request.GET.get("direction_id")
    exclude_appointment_id = request.GET.get("exclude_appointment_id")

    if not doctor_id or not direction_id:
        return JsonResponse({"dates": []})

    try:
        doctor = Doctor.objects.get(id=doctor_id)
        direction = Direction.objects.get(id=direction_id)
    except (Doctor.DoesNotExist, Direction.DoesNotExist):
        return JsonResponse({"dates": []})

    exclude_id = None
    if exclude_appointment_id:
        try:
            exclude_id = int(exclude_appointment_id)
        except ValueError:
            exclude_id = None

    result = get_available_dates_for_doctor_direction(
        doctor,
        direction,
        exclude_appointment_id=exclude_id,
    )
    return JsonResponse({"dates": result})
