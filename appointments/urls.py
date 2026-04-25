from __future__ import annotations

from django.urls import path

from appointments.views import (
    appointment_cancel_view,
    appointment_create_view,
    appointment_detail_view,
    appointment_list_view,
    available_dates,
    available_doctors,
    available_slots,
    support_appointment_create_view,
    support_appointment_list_view,
    support_appointment_update_view, doctor,
)
from appointments.views.doctor import doctor_appointment_list_view

app_name = "appointments"

urlpatterns = [
    path("create/", appointment_create_view, name="appointment_create"),
    path("", appointment_list_view, name="appointment_list"),
    path("<int:appointment_id>/", appointment_detail_view, name="appointment_detail"),
    path("<int:appointment_id>/cancel/", appointment_cancel_view, name="appointment_cancel"),
    path("ajax/load-doctors/", available_doctors, name="available_doctors"),
    path("ajax/load-dates/", available_dates, name="available_dates"),
    path("ajax/load-slots/", available_slots, name="available_slots"),
    path("staff/", support_appointment_list_view, name="support_appointment_list"),
    path("staff/create/", support_appointment_create_view, name="support_appointment_create"),
    path(
        "staff/<int:appointment_id>/edit/",
        support_appointment_update_view,
        name="support_appointment_update",
    ),

    path("doctor/", doctor.doctor_appointment_list_view, name="doctor_appointment_list"),
    path("doctor/update/<int:appointment_id>/", doctor.doctor_appointment_update_view,
         name="doctor_appointment_update"),
    path("doctor/schedule/", doctor.doctor_schedule_list_view, name="doctor_schedule_list"),
    path("doctor/schedule/create/", doctor.doctor_schedule_create_view, name="doctor_schedule_create"),
    path("doctor/schedule/update/<int:pk>/", doctor.doctor_schedule_update_view, name="doctor_schedule_update"),
]
