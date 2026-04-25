from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from appointments.models import Appointment, AppointmentStatus
from appointments.forms import SupportAppointmentUpdateForm
from doctors.models import DoctorWorkDay
from doctors.forms import DoctorWorkDayForm, DoctorWorkPeriodFormSet

@login_required
def doctor_appointment_list_view(request: HttpRequest) -> HttpResponse:
    """Список прийомів конкретного лікаря"""
    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related("user", "direction").order_by("-appointment_date")

    return render(request, "avelon_healthcare/appointments/pages/doctor_appointment_list.html", {
        "appointments": appointments
    })


@login_required
def doctor_appointment_update_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """Обробка прийому лікарем (аналог staff_update)"""
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=request.user.doctor_profile
    )

    if request.method == "POST":
        form = SupportAppointmentUpdateForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            updated_appointment = form.save(commit=False)

            # Якщо статус "Завершено", перевіряємо наявність висновку
            if updated_appointment.status == AppointmentStatus.COMPLETED:
                updated_appointment.save()
                messages.success(request, "Прийом успішно завершено, висновок збережено.")
            else:
                updated_appointment.save()
                messages.success(request, "Статус прийому оновлено.")

            return redirect("appointments:doctor_appointment_list")
    else:
        form = SupportAppointmentUpdateForm(instance=appointment)

    return render(request, "avelon_healthcare/appointments/pages/doctor_appointment_update.html", {
        "form": form,
        "appointment": appointment,
    })



@login_required
def doctor_schedule_list_view(request: HttpRequest) -> HttpResponse:
    """Перегляд власного графіка лікаря"""
    doctor = request.user.doctor_profile
    workdays = DoctorWorkDay.objects.filter(
        doctor=doctor
    ).prefetch_related("periods", "direction").order_by("-work_date")

    return render(request, "avelon_healthcare/doctors/pages/doctor_schedule_list.html", {
        "workdays": workdays
    })


@login_required
def doctor_schedule_create_view(request: HttpRequest) -> HttpResponse:
    """Створення графіка (лікар створює сам для себе)"""
    doctor = request.user.doctor_profile

    if request.method == "POST":
        form = DoctorWorkDayForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.doctor = doctor
            formset = DoctorWorkPeriodFormSet(request.POST, instance=schedule)

            if formset.is_valid():
                schedule.save()
                formset.save()
                messages.success(request, "Робочий день успішно додано до графіка.")
                return redirect("appointments:doctor_schedule_list")
    else:
        form = DoctorWorkDayForm(initial={'doctor': doctor})
        formset = DoctorWorkPeriodFormSet()

    return render(request, "avelon_healthcare/doctors/pages/doctor_schedule_form.html", {
        "form": form,
        "formset": formset,
        "is_create": True
    })


@login_required
def doctor_schedule_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Редагування власного графіка"""
    schedule = get_object_or_404(DoctorWorkDay, pk=pk, doctor=request.user.doctor_profile)

    if request.method == "POST":
        form = DoctorWorkDayForm(request.POST, instance=schedule)
        formset = DoctorWorkPeriodFormSet(request.POST, instance=schedule)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Графік успішно оновлено.")
            return redirect("appointments:doctor_schedule_list")
    else:
        form = DoctorWorkDayForm(instance=schedule)
        formset = DoctorWorkPeriodFormSet(instance=schedule)

    return render(request, "avelon_healthcare/doctors/pages/doctor_schedule_form.html", {
        "form": form,
        "formset": formset,
        "schedule": schedule,
    })