from __future__ import annotations

from django.urls import path

from .views import (
    appointment_cancel_view,
    appointment_create_view,
    appointment_detail_view,
    appointment_list_view,
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
]