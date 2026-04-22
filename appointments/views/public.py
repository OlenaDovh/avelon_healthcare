from __future__ import annotations

from django.contrib import messages
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from doctors.models import Direction
from appointments.forms import AppointmentCreateForm, GuestAppointmentCreateForm
from appointments.models import Appointment
from appointments.services import (
    fill_appointment_from_guest_data,
    fill_appointment_from_user,
    save_new_appointment,
)


def appointment_create_view(request: HttpRequest) -> HttpResponse:
    form_class = AppointmentCreateForm if request.user.is_authenticated else GuestAppointmentCreateForm

    if request.method == "POST":
        form = form_class(request.POST)

        if form.is_valid():
            appointment: Appointment = form.save(commit=False)

            if request.user.is_authenticated:
                appointment = fill_appointment_from_user(
                    appointment=appointment,
                    user=request.user,
                )
            else:
                appointment = fill_appointment_from_guest_data(
                    appointment=appointment,
                    cleaned_data=form.cleaned_data,
                )

            save_new_appointment(appointment=appointment)
            messages.success(request, "Запис до лікаря успішно створено.")

            if request.user.is_authenticated:
                return redirect("appointments:appointment_list")

            return redirect("core:home")
    else:
        form = form_class()

    return render(
        request,
        "avelon_healthcare/appointments/pages/appointment_form.html",
        {
            "form": form,
            "directions": Direction.objects.annotate(
                doctors_count=Count("doctors")
            ).filter(doctors_count__gt=0).order_by("name"),
        },
    )