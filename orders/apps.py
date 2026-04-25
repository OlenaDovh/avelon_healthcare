from __future__ import annotations
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Конфігурація застосунку orders.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
