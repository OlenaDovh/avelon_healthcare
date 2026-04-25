from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from doctors.models import DoctorWorkDay


@login_required
def doctor_schedule_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список робочих днів поточного лікаря.

    Args:
        request: HTTP-запит.

    Returns:
        HttpResponse: Відповідь зі сторінкою графіка лікаря.
    """
    doctor = request.user.doctor_profile

    workdays = DoctorWorkDay.objects.filter(
        doctor=doctor
    ).prefetch_related("periods", "direction").order_by("-work_date")

    return render(request, "avelon_healthcare/doctors/pages/doctor_schedule_list.html", {
        "workdays": workdays
    })
