"""Модуль doctors/views/public.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from accounts.permissions import head_manager_required
from doctors.forms import DoctorWorkDayForm, DoctorWorkPeriodFormSet, DirectionForm, DoctorForm
from doctors.models import Direction, Doctor, DoctorWorkDay
logger = logging.getLogger(__name__)

def doctor_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `doctor_list_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    query: str = request.GET.get('q', '').strip()
    position: str = request.GET.get('position', '').strip()
    doctors: QuerySet[Doctor] = Doctor.objects.prefetch_related('directions').all()
    if query:
        doctors = doctors.filter(Q(last_name__icontains=query) | Q(first_name__icontains=query) | Q(middle_name__icontains=query))
    if position:
        doctors = doctors.filter(position__icontains=position)
    positions: QuerySet[Doctor] = Doctor.objects.order_by('position').values_list('position', flat=True).distinct()
    logger.info('Відкрито сторінку списку лікарів.')
    return render(request, 'avelon_healthcare/doctors/pages/doctor_list.html', {'doctors': doctors, 'positions': positions, 'query': query, 'selected_position': position})

def doctor_detail_view(request: HttpRequest, doctor_id: int) -> HttpResponse:
    """Виконує логіку `doctor_detail_view`.

Args:
    request: Вхідне значення для виконання операції.
    doctor_id: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    doctor: Doctor = get_object_or_404(Doctor.objects.prefetch_related('directions'), id=doctor_id)
    logger.info('Відкрито сторінку лікаря: %s', doctor.full_name)
    return render(request, 'avelon_healthcare/doctors/pages/doctor_detail.html', {'doctor': doctor})

def direction_list_view(request: HttpRequest) -> HttpResponse:
    """Виконує логіку `direction_list_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    directions: QuerySet[Direction] = Direction.objects.all()
    logger.info('Відкрито сторінку списку напрямів.')
    return render(request, 'avelon_healthcare/doctors/pages/direction_list.html', {'directions': directions})

def direction_detail_view(request: HttpRequest, direction_id: int) -> HttpResponse:
    """Виконує логіку `direction_detail_view`.

Args:
    request: Вхідне значення для виконання операції.
    direction_id: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    direction: Direction = get_object_or_404(Direction.objects.prefetch_related('doctors'), id=direction_id)
    doctors: QuerySet[Doctor] = direction.doctors.all()
    logger.info('Відкрито сторінку напряму: %s', direction.name)
    return render(request, 'avelon_healthcare/doctors/pages/direction_detail.html', {'direction': direction, 'doctors': doctors})
