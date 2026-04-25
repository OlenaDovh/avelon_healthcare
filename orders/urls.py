"""Модуль `orders/urls.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.urls import path

from orders.views import (
    order_cancel_view,
    order_create_view,
    order_detail_view,
    order_invoice_view,
    order_list_view,
    order_pay_view,
    support_order_create_view,
    support_order_list_view,
    support_order_update_view,
)

app_name = "orders"

urlpatterns = [
    path("create/", order_create_view, name="order_create"),
    path("", order_list_view, name="order_list"),
    path("<int:order_id>/", order_detail_view, name="order_detail"),
    path("<int:order_id>/pay/", order_pay_view, name="order_pay"),
    path("<int:order_id>/cancel/", order_cancel_view, name="order_cancel"),
    path("<int:order_id>/invoice/", order_invoice_view, name="order_invoice"),
    path("staff/", support_order_list_view, name="support_order_list"),
    path("staff/create/", support_order_create_view, name="support_order_create"),
    path("staff/<int:order_id>/edit/", support_order_update_view, name="support_order_update"),
]
