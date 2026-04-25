from __future__ import annotations
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from appointments.models import Appointment, AppointmentStatus

@login_required
def appointment_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `appointment_list_view`.

Args:
    request: Вхідний параметр `request`.

Returns:
    Any: Результат виконання."""
    appointments = Appointment.objects.select_related('doctor', 'direction').filter(user=request.user).order_by('-appointment_date', '-appointment_time')
    return render(request, 'avelon_healthcare/appointments/pages/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_detail_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """Виконує логіку `appointment_detail_view`.

Args:
    request: Вхідний параметр `request`.
    appointment_id: Вхідний параметр `appointment_id`.

Returns:
    Any: Результат виконання."""
    appointment = get_object_or_404(Appointment.objects.select_related('doctor', 'direction', 'user'), id=appointment_id, user=request.user)
    return render(request, 'avelon_healthcare/appointments/pages/appointment_detail.html', {'appointment': appointment})

@login_required
def appointment_cancel_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """Виконує логіку `appointment_cancel_view`.

Args:
    request: Вхідний параметр `request`.
    appointment_id: Вхідний параметр `appointment_id`.

Returns:
    Any: Результат виконання."""
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if appointment.status == AppointmentStatus.PLANNED:
        appointment.status = AppointmentStatus.REJECTED
        appointment.save(update_fields=['status'])
        messages.success(request, 'Запис успішно скасовано.')
    else:
        messages.warning(request, "Скасувати можна лише запис зі статусом 'Заплановано'.")
    return redirect('appointments:appointment_list')
