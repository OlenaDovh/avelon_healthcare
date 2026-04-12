from __future__ import annotations

import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from doctors.models import Direction, Doctor

from .forms import AppointmentCreateForm, GuestAppointmentCreateForm
from .models import Appointment, AppointmentStatus
from .utils import get_available_slots_for_doctor_on_date, send_appointment_email

logger = logging.getLogger(__name__)


def appointment_create_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає та обробляє форму запису до лікаря.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь або редірект.
    """
    form_class = AppointmentCreateForm if request.user.is_authenticated else GuestAppointmentCreateForm

    if request.method == "POST":
        form = form_class(request.POST)

        if form.is_valid():
            appointment: Appointment = form.save(commit=False)

            if request.user.is_authenticated:
                appointment.user = request.user
                appointment.full_name = request.user.get_full_name() or request.user.username
                appointment.phone = getattr(request.user, "phone", "") or ""
                appointment.email = request.user.email or ""
            else:
                appointment.user = None
                appointment.full_name = form.cleaned_data["full_name"]
                appointment.phone = form.cleaned_data["phone"]
                appointment.email = form.cleaned_data["email"]

            appointment.save()
            send_appointment_email(appointment)

            logger.info(
                "Створено запис до лікаря. patient=%s doctor=%s date=%s time=%s",
                appointment.customer_name,
                appointment.doctor.full_name,
                appointment.appointment_date,
                appointment.appointment_time,
            )

            messages.success(request, "Запис до лікаря успішно створено.")

            if request.user.is_authenticated:
                return redirect("appointments:appointment_list")

            return redirect("core:home")

        logger.warning("Неуспішна спроба створення запису до лікаря.")
    else:
        form = form_class()

    return render(
        request,
        "avelon_healthcare/appointments/appointment_form.html",
        {
            "form": form,
            "directions": Direction.objects.annotate(
                doctors_count=Count("doctors")
            ).filter(doctors_count__gt=0).order_by("name"),
        },
    )


@login_required
def appointment_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список записів поточного користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі списком записів.
    """
    appointments = (
        Appointment.objects.select_related("doctor", "direction")
        .filter(user=request.user)
        .order_by("-appointment_date", "-appointment_time")
    )

    logger.info("Відкрито список записів користувача: %s", request.user.username)

    return render(
        request,
        "avelon_healthcare/appointments/appointment_list.html",
        {"appointments": appointments},
    )


@login_required
def appointment_detail_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """
    Відображає детальну інформацію про запис до лікаря.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        appointment_id (int): Ідентифікатор запису.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою деталей запису.
    """
    appointment: Appointment = get_object_or_404(
        Appointment.objects.select_related("doctor", "direction", "user"),
        id=appointment_id,
        user=request.user,
    )

    logger.info(
        "Відкрито деталі запису. user=%s appointment_id=%s",
        request.user.username,
        appointment.id,
    )

    return render(
        request,
        "avelon_healthcare/appointments/appointment_detail.html",
        {"appointment": appointment},
    )


@login_required
def appointment_cancel_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """
    Скасовує запис до лікаря поточного користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        appointment_id (int): Ідентифікатор запису.

    Returns:
        HttpResponse: Редірект на список записів.
    """
    appointment: Appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        user=request.user,
    )

    if appointment.status == AppointmentStatus.PLANNED:
        appointment.status = AppointmentStatus.REJECTED
        appointment.save(update_fields=["status"])

        logger.info(
            "Скасовано запис до лікаря. user=%s appointment_id=%s",
            request.user.username,
            appointment.id,
        )

        messages.success(request, "Запис успішно скасовано.")
    else:
        logger.warning(
            "Спроба скасувати запис з неактивним статусом. user=%s appointment_id=%s",
            request.user.username,
            appointment.id,
        )
        messages.warning(
            request,
            "Скасувати можна лише запис зі статусом 'Заплановано'.",
        )

    return redirect("appointments:appointment_list")


def available_slots(request: HttpRequest) -> JsonResponse:
    """
    Повертає доступні часові слоти.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        JsonResponse: JSON зі слотами.
    """
    doctor_id = request.GET.get("doctor_id")
    direction_id = request.GET.get("direction_id")
    appointment_date = request.GET.get("date")

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

    slots = get_available_slots_for_doctor_on_date(doctor, direction, selected_date)
    return JsonResponse({"slots": slots})


def available_doctors(request: HttpRequest) -> JsonResponse:
    """
    Повертає список лікарів за напрямом.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        JsonResponse: JSON зі списком лікарів.
    """
    direction_id = request.GET.get("direction_id")

    if not direction_id:
        return JsonResponse({"doctors": []})

    doctors = Doctor.objects.filter(
        directions__id=direction_id
    ).distinct().order_by("full_name")

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


def available_dates(request: HttpRequest) -> JsonResponse:
    """
    Повертає доступні дати для лікаря.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        JsonResponse: JSON зі списком дат.
    """
    doctor_id = request.GET.get("doctor_id")
    direction_id = request.GET.get("direction_id")

    if not doctor_id or not direction_id:
        return JsonResponse({"dates": []})

    try:
        doctor = Doctor.objects.get(id=doctor_id)
        direction = Direction.objects.get(id=direction_id)
    except (Doctor.DoesNotExist, Direction.DoesNotExist):
        return JsonResponse({"dates": []})

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
        )
        if slots:
            result.append(workday.work_date.strftime("%Y-%m-%d"))

    return JsonResponse({"dates": result})