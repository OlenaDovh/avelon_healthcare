from __future__ import annotations

from django.urls import path

from . import views
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
    path("head-manager/doctors/", views.head_manager_doctor_list_view, name="head_manager_doctor_list"),
    path("head-manager/doctors/create/", views.head_manager_doctor_create_view, name="head_manager_doctor_create"),
    path("head-manager/doctors/<int:pk>/update/", views.head_manager_doctor_update_view,
         name="head_manager_doctor_update"),

    path("head-manager/directions/", views.head_manager_direction_list_view, name="head_manager_direction_list"),
    path("head-manager/directions/create/", views.head_manager_direction_create_view,
         name="head_manager_direction_create"),
    path("head-manager/directions/<int:pk>/update/", views.head_manager_direction_update_view,
         name="head_manager_direction_update"),

    path("head-manager/schedules/", views.head_manager_schedule_list_view, name="head_manager_schedule_list"),
    path("head-manager/schedules/create/", views.head_manager_schedule_create_view,
         name="head_manager_schedule_create"),
    path("head-manager/schedules/<int:pk>/update/", views.head_manager_schedule_update_view,
         name="head_manager_schedule_update"),
    path(
        "head-manager/ajax/load-doctor-directions/",
        views.head_manager_load_doctor_directions_view,
        name="head_manager_load_doctor_directions",
    ),
]
