"""Модуль `appointments/views/patient.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from appointments.models import Appointment, AppointmentStatus


@login_required
def appointment_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `appointment_list_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    appointments = (
        Appointment.objects.select_related("doctor", "direction")
        .filter(user=request.user)
        .order_by("-appointment_date", "-appointment_time")
    )

    return render(
        request,
        "avelon_healthcare/appointments/pages/appointment_list.html",
        {"appointments": appointments},
    )


@login_required
def appointment_detail_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """Виконує прикладну логіку функції `appointment_detail_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        appointment_id: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    appointment = get_object_or_404(
        Appointment.objects.select_related("doctor", "direction", "user"),
        id=appointment_id,
        user=request.user,
    )

    return render(
        request,
        "avelon_healthcare/appointments/pages/appointment_detail.html",
        {"appointment": appointment},
    )


@login_required
def appointment_cancel_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """Виконує прикладну логіку функції `appointment_cancel_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        appointment_id: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        user=request.user,
    )

    if appointment.status == AppointmentStatus.PLANNED:
        appointment.status = AppointmentStatus.REJECTED
        appointment.save(update_fields=["status"])
        messages.success(request, "Запис успішно скасовано.")
    else:
        messages.warning(request, "Скасувати можна лише запис зі статусом 'Заплановано'.")

    return redirect("appointments:appointment_list")
