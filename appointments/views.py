from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AppointmentCreateForm
from .models import Appointment, AppointmentStatus

logger = logging.getLogger(__name__)


@login_required
def appointment_create_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає та обробляє форму запису до лікаря.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь або редірект.
    """
    if request.method == "POST":
        form = AppointmentCreateForm(request.POST)

        if form.is_valid():
            appointment: Appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()

            logger.info(
                "Створено запис до лікаря. user=%s doctor=%s date=%s time=%s",
                request.user.username,
                appointment.doctor.full_name,
                appointment.appointment_date,
                appointment.appointment_time,
            )

            messages.success(request, "Запис до лікаря успішно створено.")
            return redirect("appointments:appointment_list")
        logger.warning(
            "Неуспішна спроба створення запису до лікаря. user=%s",
            request.user.username,
        )
    else:
        form = AppointmentCreateForm()

    return render(
        request,
        "avelon_healthcare/appointments/appointment_form.html",
        {"form": form},
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