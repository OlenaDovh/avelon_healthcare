from __future__ import annotations
from django.apps import AppConfig


class DoctorsConfig(AppConfig):
    """
    Конфігурація застосунку doctors.

    Визначає базові налаштування застосунку.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "doctors"
