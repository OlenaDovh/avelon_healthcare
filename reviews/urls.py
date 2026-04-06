from __future__ import annotations

from django.urls import path

from .views import review_create_view, review_list_view

app_name = "reviews"

urlpatterns = [
    path("", review_list_view, name="review_list"),
    path("create/<int:appointment_id>/", review_create_view, name="review_create"),
]