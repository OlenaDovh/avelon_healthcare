from __future__ import annotations

from django.urls import path

from .views import (
    order_cancel_view,
    order_create_view,
    order_detail_view,
    order_list_view,
)

app_name = "orders"

urlpatterns = [
    path("create/", order_create_view, name="order_create"),
    path("", order_list_view, name="order_list"),
    path("<int:order_id>/", order_detail_view, name="order_detail"),
    path("<int:order_id>/cancel/", order_cancel_view, name="order_cancel"),
]