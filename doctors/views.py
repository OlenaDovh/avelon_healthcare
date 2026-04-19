from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from accounts.permissions import head_manager_required
from .forms import DoctorWorkDayForm, DoctorWorkPeriodFormSet, DirectionForm, DoctorForm
from .models import Direction, Doctor, DoctorWorkDay

logger = logging.getLogger(__name__)


def doctor_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список лікарів з пошуком і фільтром.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі списком лікарів.
    """
    query: str = request.GET.get("q", "").strip()
    position: str = request.GET.get("position", "").strip()

    doctors: QuerySet[Doctor] = Doctor.objects.prefetch_related("directions").all()

    if query:
        doctors = doctors.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query)
        )

    if position:
        doctors = doctors.filter(position__icontains=position)

    positions: QuerySet[Doctor] = Doctor.objects.order_by("position").values_list(
        "position",
        flat=True,
    ).distinct()

    logger.info("Відкрито сторінку списку лікарів.")

    return render(
        request,
        "avelon_healthcare/doctors/doctor_list.html",
        {
            "doctors": doctors,
            "positions": positions,
            "query": query,
            "selected_position": position,
        },
    )


def doctor_detail_view(request: HttpRequest, doctor_id: int) -> HttpResponse:
    """
    Відображає детальну інформацію про лікаря.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        doctor_id (int): Ідентифікатор лікаря.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою лікаря.
    """
    doctor: Doctor = get_object_or_404(
        Doctor.objects.prefetch_related("directions"),
        id=doctor_id,
    )

    logger.info("Відкрито сторінку лікаря: %s", doctor.full_name)

    return render(
        request,
        "avelon_healthcare/doctors/doctor_detail.html",
        {"doctor": doctor},
    )


def direction_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список напрямів клініки.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі списком напрямів.
    """
    directions: QuerySet[Direction] = Direction.objects.all()

    logger.info("Відкрито сторінку списку напрямів.")

    return render(
        request,
        "avelon_healthcare/doctors/direction_list.html",
        {"directions": directions},
    )


def direction_detail_view(request: HttpRequest, direction_id: int) -> HttpResponse:
    """
    Відображає детальну інформацію про напрям і список лікарів цього напряму.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        direction_id (int): Ідентифікатор напряму.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою напряму.
    """
    direction: Direction = get_object_or_404(
        Direction.objects.prefetch_related("doctors"),
        id=direction_id,
    )

    doctors: QuerySet[Doctor] = direction.doctors.all()

    logger.info("Відкрито сторінку напряму: %s", direction.name)

    return render(
        request,
        "avelon_healthcare/doctors/direction_detail.html",
        {
            "direction": direction,
            "doctors": doctors,
        },
    )

@login_required
@head_manager_required
def head_manager_doctor_list_view(request: HttpRequest) -> HttpResponse:
    doctors = Doctor.objects.prefetch_related("directions").all()

    return render(
        request,
        "avelon_healthcare/doctors/head_manager_doctor_list.html",
        {"doctors": doctors},
    )


@login_required
@head_manager_required
def head_manager_doctor_create_view(request: HttpRequest) -> HttpResponse:
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
        "avelon_healthcare/doctors/head_manager_doctor_form.html",
        {"form": form},
    )


@login_required
@head_manager_required
def head_manager_doctor_update_view(request: HttpRequest, pk: int) -> HttpResponse:
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
        "avelon_healthcare/doctors/head_manager_doctor_form.html",
        {
            "form": form,
            "doctor": doctor,
        },
    )


@login_required
@head_manager_required
def head_manager_direction_list_view(request: HttpRequest) -> HttpResponse:
    directions = Direction.objects.all()

    return render(
        request,
        "avelon_healthcare/doctors/head_manager_direction_list.html",
        {"directions": directions},
    )


@login_required
@head_manager_required
def head_manager_direction_create_view(request: HttpRequest) -> HttpResponse:
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
        "avelon_healthcare/doctors/head_manager_direction_form.html",
        {"form": form},
    )


@login_required
@head_manager_required
def head_manager_direction_update_view(request: HttpRequest, pk: int) -> HttpResponse:
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
        "avelon_healthcare/doctors/head_manager_direction_form.html",
        {
            "form": form,
            "direction": direction,
        },
    )


@login_required
@head_manager_required
def head_manager_schedule_list_view(request: HttpRequest) -> HttpResponse:
    schedules = (
        DoctorWorkDay.objects.select_related("doctor", "direction")
        .prefetch_related("periods")
        .order_by("-work_date", "doctor__last_name", "doctor__first_name")
    )

    return render(
        request,
        "avelon_healthcare/doctors/head_manager_schedule_list.html",
        {"schedules": schedules},
    )


@login_required
@head_manager_required
def head_manager_schedule_create_view(request: HttpRequest) -> HttpResponse:
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
        "avelon_healthcare/doctors/head_manager_schedule_form.html",
        {
            "form": form,
            "formset": formset,
        },
    )


@login_required
@head_manager_required
def head_manager_schedule_update_view(request: HttpRequest, pk: int) -> HttpResponse:
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
        "avelon_healthcare/doctors/head_manager_schedule_form.html",
        {
            "form": form,
            "formset": formset,
            "schedule": schedule,
        },
    )

@login_required
@head_manager_required
def head_manager_load_doctor_directions_view(request: HttpRequest) -> JsonResponse:
    doctor_id = request.GET.get("doctor_id")

    directions_data: list[dict[str, str | int]] = []

    if doctor_id:
        directions = Direction.objects.filter(
            doctors__id=doctor_id
        ).distinct().order_by("name")

        directions_data = [
            {
                "id": direction.id,
                "name": direction.name,
            }
            for direction in directions
        ]

    return JsonResponse({"directions": directions_data})