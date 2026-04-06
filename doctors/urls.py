from __future__ import annotations

from django.urls import path

from .views import (
    direction_detail_view,
    direction_list_view,
    doctor_detail_view,
    doctor_list_view,
)

app_name = "doctors"

urlpatterns = [
    path("", doctor_list_view, name="doctor_list"),
    path("<int:doctor_id>/", doctor_detail_view, name="doctor_detail"),
    path("directions/", direction_list_view, name="direction_list"),
    path("directions/<int:direction_id>/", direction_detail_view, name="direction_detail"),
]