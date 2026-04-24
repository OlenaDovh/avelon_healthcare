from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from doctors.models import DoctorWorkDay


@login_required
def doctor_schedule_list_view(request):
    doctor = request.user.doctor_profile

    workdays = DoctorWorkDay.objects.filter(
        doctor=doctor
    ).prefetch_related("periods", "direction").order_by("-work_date")

    return render(request, "doctors/pages/doctor_schedule_list.html", {
        "workdays": workdays
    })