from __future__ import annotations
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from appointments.models import Appointment, AppointmentStatus
from reviews.forms import ReviewCreateForm
from reviews.models import Review

logger = logging.getLogger(__name__)


def review_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список відгуків з пагінацією.

    Args:
        request: HTTP-запит.

    Returns:
        HttpResponse: Відповідь зі сторінкою списку відгуків.
    """
    reviews_qs = Review.objects.select_related("user", "appointment")

    paginator = Paginator(reviews_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "avelon_healthcare/reviews/pages/review_list.html",
        {"page_obj": page_obj},
    )


@login_required
def review_create_view(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """
    Обробляє створення відгуку для завершеного прийому.

    Args:
        request: HTTP-запит.
        appointment_id: Ідентифікатор прийому.

    Returns:
        HttpResponse: Відповідь зі сторінкою форми або перенаправленням.
    """
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        user=request.user,
    )

    if appointment.status != AppointmentStatus.COMPLETED:
        messages.warning(request, "Відгук можна залишити лише для завершеного прийому.")
        return redirect("appointments:appointment_detail", appointment_id=appointment.id)

    if hasattr(appointment, "review"):
        messages.warning(request, "Для цього прийому відгук уже створено.")
        return redirect("appointments:appointment_detail", appointment_id=appointment.id)

    if request.method == "POST":
        form = ReviewCreateForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.appointment = appointment
            review.full_clean()
            review.save()

            return redirect("reviews:review_list")
    else:
        form = ReviewCreateForm()

    return render(
        request,
        "avelon_healthcare/reviews/pages/review_form.html",
        {
            "form": form,
            "appointment": appointment,
        },
    )