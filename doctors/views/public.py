from __future__ import annotations
import logging
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from doctors.models import Direction, Doctor

logger = logging.getLogger(__name__)


def doctor_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список лікарів з пошуком і фільтром.

    Args:
        request: HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі списком лікарів.
    """
    query = request.GET.get("q", "").strip()
    position = request.GET.get("position", "").strip()

    doctors = Doctor.objects.prefetch_related("directions").all()

    if query:
        doctors = doctors.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query)
        )

    if position:
        doctors = doctors.filter(position__icontains=position)

    positions = Doctor.objects.order_by("position").values_list(
        "position",
        flat=True,
    ).distinct()

    logger.info("Відкрито сторінку списку лікарів.")

    return render(
        request,
        "avelon_healthcare/doctors/pages/doctor_list.html",
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
        request: HTTP-запит користувача.
        doctor_id: Ідентифікатор лікаря.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою лікаря.
    """
    doctor = get_object_or_404(
        Doctor.objects.prefetch_related("directions"),
        id=doctor_id,
    )

    logger.info("Відкрито сторінку лікаря: %s", doctor.full_name)

    return render(
        request,
        "avelon_healthcare/doctors/pages/doctor_detail.html",
        {"doctor": doctor},
    )


def direction_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список напрямів клініки.

    Args:
        request: HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі списком напрямів.
    """
    directions = Direction.objects.all()

    logger.info("Відкрито сторінку списку напрямів.")

    return render(
        request,
        "avelon_healthcare/doctors/pages/direction_list.html",
        {"directions": directions},
    )


def direction_detail_view(request: HttpRequest, direction_id: int) -> HttpResponse:
    """
    Відображає детальну інформацію про напрям і список лікарів цього напряму.

    Args:
        request: HTTP-запит користувача.
        direction_id: Ідентифікатор напряму.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою напряму.
    """
    direction = get_object_or_404(
        Direction.objects.prefetch_related("doctors"),
        id=direction_id,
    )

    doctors = direction.doctors.all()

    logger.info("Відкрито сторінку напряму: %s", direction.name)

    return render(
        request,
        "avelon_healthcare/doctors/pages/direction_detail.html",
        {
            "direction": direction,
            "doctors": doctors,
        },
    )
