"""Модуль `doctors/views/head_manager.py` застосунку `doctors`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from accounts.permissions import head_manager_required
from doctors.forms import DoctorForm, DirectionForm, DoctorWorkDayForm, DoctorWorkPeriodFormSet
from doctors.models import Direction, Doctor, DoctorWorkDay

logger = logging.getLogger(__name__)

@login_required
@head_manager_required
def head_manager_doctor_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `head_manager_doctor_list_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    doctors = Doctor.objects.prefetch_related("directions").all()

    return render(
        request,
        "avelon_healthcare/doctors/pages/head_manager_doctor_list.html",
        {"doctors": doctors},
    )


@login_required
@head_manager_required
def head_manager_doctor_create_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `head_manager_doctor_create_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Лікаря успішно створено.")
            return redirect("doctors:head_manager_doctor_list")
    else:
        form = DoctorForm()

    return render(
        request,
        "avelon_healthcare/doctors/pages/head_manager_doctor_form.html",
        {"form": form},
    )


@login_required
@head_manager_required
def head_manager_doctor_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Виконує прикладну логіку функції `head_manager_doctor_update_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        pk: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Дані лікаря успішно оновлено.")
            return redirect("doctors:head_manager_doctor_list")
    else:
        form = DoctorForm(instance=doctor)

    return render(
        request,
        "avelon_healthcare/doctors/pages/head_manager_doctor_form.html",
        {
            "form": form,
            "doctor": doctor,
        },
    )


@login_required
@head_manager_required
def head_manager_direction_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `head_manager_direction_list_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    directions = Direction.objects.all()

    return render(
        request,
        "avelon_healthcare/doctors/pages/head_manager_direction_list.html",
        {"directions": directions},
    )


@login_required
@head_manager_required
def head_manager_direction_create_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `head_manager_direction_create_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if request.method == "POST":
        form = DirectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Напрям успішно створено.")
            return redirect("doctors:head_manager_direction_list")
    else:
        form = DirectionForm()

    return render(
        request,
        "avelon_healthcare/doctors/pages/head_manager_direction_form.html",
        {"form": form},
    )


@login_required
@head_manager_required
def head_manager_direction_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Виконує прикладну логіку функції `head_manager_direction_update_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        pk: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    direction = get_object_or_404(Direction, pk=pk)

    if request.method == "POST":
        form = DirectionForm(request.POST, instance=direction)
        if form.is_valid():
            form.save()
            messages.success(request, "Напрям успішно оновлено.")
            return redirect("doctors:head_manager_direction_list")
    else:
        form = DirectionForm(instance=direction)

    return render(
        request,
        "avelon_healthcare/doctors/pages/head_manager_direction_form.html",
        {
            "form": form,
            "direction": direction,
        },
    )


@login_required
@head_manager_required
def head_manager_schedule_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `head_manager_schedule_list_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    schedules = (
        DoctorWorkDay.objects.select_related("doctor", "direction")
        .prefetch_related("periods")
        .order_by("-work_date", "doctor__last_name", "doctor__first_name")
    )

    return render(
        request,
        "avelon_healthcare/doctors/pages/head_manager_schedule_list.html",
        {"schedules": schedules},
    )


@login_required
@head_manager_required
def head_manager_schedule_create_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `head_manager_schedule_create_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if request.method == "POST":
        form = DoctorWorkDayForm(request.POST)
        formset = DoctorWorkPeriodFormSet(request.POST)

        if form.is_valid():
            schedule = form.save(commit=False)
            formset = DoctorWorkPeriodFormSet(request.POST, instance=schedule)

            if formset.is_valid():
                schedule.save()
                form.save_m2m() if hasattr(form, "save_m2m") else None
                formset.instance = schedule
                formset.save()
                messages.success(request, "Графік успішно створено.")
                return redirect("doctors:head_manager_schedule_list")
    else:
        form = DoctorWorkDayForm()
        formset = DoctorWorkPeriodFormSet()

    return render(
        request,
        "avelon_healthcare/doctors/pages/head_manager_schedule_form.html",
        {
            "form": form,
            "formset": formset,
        },
    )


@login_required
@head_manager_required
def head_manager_schedule_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Виконує прикладну логіку функції `head_manager_schedule_update_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        pk: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    schedule = get_object_or_404(DoctorWorkDay, pk=pk)

    if request.method == "POST":
        form = DoctorWorkDayForm(request.POST, instance=schedule)
        formset = DoctorWorkPeriodFormSet(request.POST, instance=schedule)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Графік успішно оновлено.")
            return redirect("doctors:head_manager_schedule_list")
    else:
        form = DoctorWorkDayForm(instance=schedule)
        formset = DoctorWorkPeriodFormSet(instance=schedule)

    return render(
        request,
        "avelon_healthcare/doctors/pages/head_manager_schedule_form.html",
        {
            "form": form,
            "formset": formset,
            "schedule": schedule,
        },
    )
