from __future__ import annotations
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Конфігурація застосунку core.

    Визначає базові налаштування застосунку.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
