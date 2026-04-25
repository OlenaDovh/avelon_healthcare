from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from appointments.models import Appointment

@login_required
def doctor_appointment_list_view(request):
    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related("user", "direction").order_by("-appointment_date")

    return render(request, "avelon_healthcare/appointments/pages/doctor_appointment_list.html", {
        "appointments": appointments
    })