from __future__ import annotations

import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from accounts.permissions import support_required
from doctors.models import Direction, Doctor

from .forms import (
    AppointmentCreateForm,
    GuestAppointmentCreateForm,
    SupportAppointmentCreateForm,
    SupportAppointmentUpdateForm,
)
from .models import Appointment, AppointmentStatus
from .utils import (
    get_available_dates_for_doctor_direction,
    get_available_slots_for_doctor_on_date,
    send_appointment_email,
)

logger = logging.getLogger(__name__)

User = get_user_model()
PATIENT_GROUP_NAME = "patient"


def appointment_create_view(request: HttpRequest) -> HttpResponse:
    form_class = AppointmentCreateForm if request.user.is_authenticated else GuestAppointmentCreateForm

    if request.method == "POST":
        form = form_class(request.POST)

        if form.is_valid():
            appointment: Appointment = form.save(commit=False)

            if request.user.is_authenticated:
                appointment.user = request.user
                appointment.last_name = request.user.last_name
                appointment.first_name = request.user.first_name
                appointment.middle_name = getattr(request.user, "middle_name", "") or ""
                appointment.phone = getattr(request.user, "phone", "") or ""
                appointment.email = request.user.email or ""
            else:
                appointment.user = None
                appointment.last_name = form.cleaned_data["last_name"]
                appointment.first_name = form.cleaned_data["first_name"]
                appointment.middle_name = form.cleaned_data["middle_name"]
                appointment.phone = form.cleaned_data["phone"]
                appointment.email = form.cleaned_data["email"]

            appointment.save()
            send_appointment_email(appointment)

            messages.success(request, "Запис до лікаря успішно створено.")

            if request.user.is_authenticated:
                return redirect("appointments:appointment_list")

            return redirect("core:home")
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
    appointments = (
        Appointment.objects.select_related("doctor", "direction")
        .filter(user=request.user)
        .order_by("-appointment_date", "-appointment_time")
    )

    return render(
        request,
        "avelon_healthcare/appointments/appointment_list.html",
        {"appointments": appointments},
    )


@login_required
def appointment_detail_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    appointment = get_object_or_404(
        Appointment.objects.select_related("doctor", "direction", "user"),
        id=appointment_id,
        user=request.user,
    )

    return render(
        request,
        "avelon_healthcare/appointments/appointment_detail.html",
        {"appointment": appointment},
    )


@login_required
def appointment_cancel_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
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


@login_required
@support_required
def support_appointment_list_view(request: HttpRequest) -> HttpResponse:
    appointments = (
        Appointment.objects.select_related("doctor", "direction", "user")
        .filter(Q(user__isnull=True) | Q(user__groups__name=PATIENT_GROUP_NAME))
        .distinct()
        .order_by("-appointment_date", "-appointment_time")
    )

    return render(
        request,
        "avelon_healthcare/appointments/support_appointment_list.html",
        {"appointments": appointments},
    )


@login_required
@support_required
def support_appointment_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SupportAppointmentCreateForm(request.POST)

        if form.is_valid():
            appointment: Appointment = form.save(commit=False)
            user: User | None = form.cleaned_data.get("user")

            if user and not user.groups.filter(name=PATIENT_GROUP_NAME).exists():
                messages.error(request, "Можна обирати тільки користувачів із групою patient.")
                return redirect("appointments:support_appointment_create")

            if user:
                appointment.user = user
                appointment.last_name = user.last_name
                appointment.first_name = user.first_name
                appointment.middle_name = getattr(user, "middle_name", "") or ""
                appointment.phone = getattr(user, "phone", "") or ""
                appointment.email = user.email or ""
            else:
                appointment.user = None
                appointment.last_name = form.cleaned_data["last_name"]
                appointment.first_name = form.cleaned_data["first_name"]
                appointment.middle_name = form.cleaned_data["middle_name"]
                appointment.phone = form.cleaned_data["phone"]
                appointment.email = form.cleaned_data["email"]

            appointment.save()
            messages.success(request, "Запис успішно створено.")
            return redirect("appointments:support_appointment_list")
    else:
        form = SupportAppointmentCreateForm()

    users_data = [
        {
            "id": user.id,
            "full_name": user.full_name or user.username,
            "phone": getattr(user, "phone", "") or "—",
            "email": user.email or "—",
        }
        for user in patient_users_queryset().order_by("last_name", "first_name")
    ]

    return render(
        request,
        "avelon_healthcare/appointments/support_appointment_form.html",
        {
            "form": form,
            "users_data": users_data,
        },
    )

@login_required
@support_required
def support_appointment_update_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    appointment = get_object_or_404(
        Appointment.objects.select_related("user", "doctor", "direction"),
        Q(id=appointment_id)
        & (Q(user__isnull=True) | Q(user__groups__name=PATIENT_GROUP_NAME)),
    )

    if request.method == "POST":
        form = SupportAppointmentUpdateForm(request.POST, request.FILES, instance=appointment)

        if form.is_valid():
            updated_appointment = form.save(commit=False)

            if appointment.status == AppointmentStatus.REJECTED:
                messages.warning(request, "Відхилений запис редагувати не можна.")
                return redirect("appointments:support_appointment_list")

            if appointment.status == AppointmentStatus.COMPLETED:
                # Для завершеного запису дозволяємо змінювати тільки файл висновку
                updated_appointment.direction = appointment.direction
                updated_appointment.doctor = appointment.doctor
                updated_appointment.appointment_date = appointment.appointment_date
                updated_appointment.appointment_time = appointment.appointment_time
                updated_appointment.description = appointment.description
                updated_appointment.status = appointment.status
                updated_appointment.rejection_reason = appointment.rejection_reason

                updated_appointment.save(update_fields=["final_conclusion"])
                messages.success(request, "Файл висновку успішно оновлено.")
                return redirect("appointments:support_appointment_list")

            if updated_appointment.status != AppointmentStatus.REJECTED:
                updated_appointment.rejection_reason = ""

            if updated_appointment.status != AppointmentStatus.COMPLETED:
                updated_appointment.final_conclusion = None

            updated_appointment.save()
            messages.success(request, "Запис успішно оновлено.")
            return redirect("appointments:support_appointment_list")
    else:
        form = SupportAppointmentUpdateForm(instance=appointment)

    return render(
        request,
        "avelon_healthcare/appointments/support_appointment_update.html",
        {
            "form": form,
            "appointment": appointment,
        },
    )


@require_GET
def available_slots(request: HttpRequest) -> JsonResponse:
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

    exclude_id: int | None = None
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

    exclude_id: int | None = None
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