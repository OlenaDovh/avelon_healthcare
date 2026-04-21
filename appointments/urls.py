from __future__ import annotations

from django.urls import path

from .views import (
    appointment_cancel_view,
    appointment_create_view,
    appointment_detail_view,
    appointment_list_view, available_slots, available_doctors, available_dates, support_appointment_list_view,
    support_appointment_create_view, support_appointment_update_view,
)

app_name = "appointments"

urlpatterns = [
    path("create/", appointment_create_view, name="appointment_create"),
    path("", appointment_list_view, name="appointment_list"),
    path("<int:appointment_id>/", appointment_detail_view, name="appointment_detail"),
    path(
        "<int:appointment_id>/cancel/",
        appointment_cancel_view,
        name="appointment_cancel",
    ),
    path("slots/", available_slots, name="slots"),
    path("doctors/", available_doctors, name="available_doctors"),
    path("dates/", available_dates, name="available_dates"),
    path("staff/", support_appointment_list_view, name="support_appointment_list"),
    path("staff/create/", support_appointment_create_view, name="support_appointment_create"),
    path("staff/<int:appointment_id>/edit/", support_appointment_update_view, name="support_appointment_update"),
    path("ajax/load-doctors/", available_doctors, name="available_doctors"),
    path("ajax/load-dates/", available_dates, name="available_dates"),
    path("ajax/load-slots/", available_slots, name="available_slots"),
]
