from __future__ import annotations

from django.urls import path

from .views import (
    add_to_cart_view,
    analysis_list_view,
    cart_detail_view,
    remove_from_cart_view,
)

app_name = "analysis"

urlpatterns = [
    path("", analysis_list_view, name="analysis_list"),
    path("cart/", cart_detail_view, name="cart_detail"),
    path("add/<int:analysis_id>/", add_to_cart_view, name="add_to_cart"),
    path("remove/<int:analysis_id>/", remove_from_cart_view, name="remove_from_cart"),
]