from __future__ import annotations
from django.apps import AppConfig


class DailyHoroscopeConfig(AppConfig):
    """
    Конфігурація застосунку daily_horoscope.

    Визначає базові налаштування застосунку.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "daily_horoscope"
