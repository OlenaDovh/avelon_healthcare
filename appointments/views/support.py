from __future__ import annotations
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.constants import PATIENT_GROUP
from accounts.permissions import support_required
from accounts.selectors import patient_users_queryset
from appointments.forms import SupportAppointmentCreateForm, SupportAppointmentUpdateForm
from appointments.models import Appointment, AppointmentStatus

User = get_user_model()


@login_required
@support_required
def support_appointment_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список записів пацієнтів для support-користувача.

    Args:
        request: HTTP-запит.

    Returns:
        HttpResponse: Відповідь зі сторінкою списку записів.
    """
    appointments = (
        Appointment.objects.select_related("doctor", "direction", "user")
        .filter(Q(user__isnull=True) | Q(user__groups__name=PATIENT_GROUP))
        .distinct()
        .order_by("-appointment_date", "-appointment_time")
    )

    return render(
        request,
        "avelon_healthcare/appointments/pages/support_appointment_list.html",
        {"appointments": appointments},
    )


@login_required
@support_required
def support_appointment_create_view(request: HttpRequest) -> HttpResponse:
    """
    Обробляє створення запису до лікаря support-користувачем.

    Args:
        request: HTTP-запит.

    Returns:
        HttpResponse: Відповідь зі сторінкою форми або перенаправленням.
    """
    if request.method == "POST":
        form = SupportAppointmentCreateForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            user = form.cleaned_data.get("user")

            if user and not user.groups.filter(name=PATIENT_GROUP).exists():
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
        "avelon_healthcare/appointments/pages/support_appointment_form.html",
        {
            "form": form,
            "users_data": users_data,
        },
    )


@login_required
@support_required
def support_appointment_update_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """
    Обробляє оновлення запису до лікаря support-користувачем.

    Args:
        request: HTTP-запит.
        appointment_id: Ідентифікатор запису.

    Returns:
        HttpResponse: Відповідь зі сторінкою редагування запису або перенаправленням.
    """
    appointment = get_object_or_404(
        Appointment.objects.select_related("user", "doctor", "direction"),
        Q(id=appointment_id) & (Q(user__isnull=True) | Q(user__groups__name=PATIENT_GROUP)),
    )

    if request.method == "POST":
        form = SupportAppointmentUpdateForm(request.POST, request.FILES, instance=appointment)

        if form.is_valid():
            updated_appointment = form.save(commit=False)

            if appointment.status == AppointmentStatus.REJECTED:
                messages.warning(request, "Відхилений запис редагувати не можна.")
                return redirect("appointments:support_appointment_list")

            if appointment.status == AppointmentStatus.COMPLETED:
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
        "avelon_healthcare/appointments/pages/support_appointment_update.html",
        {
            "form": form,
            "appointment": appointment,
        },
    )
