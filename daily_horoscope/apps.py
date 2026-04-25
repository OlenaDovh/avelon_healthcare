from __future__ import annotations
from django.apps import AppConfig

class DailyHoroscopeConfig(AppConfig):
    """Описує клас `DailyHoroscopeConfig`."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daily_horoscope'
