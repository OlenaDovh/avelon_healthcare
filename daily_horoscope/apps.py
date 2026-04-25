"""Модуль `daily_horoscope/apps.py` застосунку `daily_horoscope`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.apps import AppConfig


class DailyHoroscopeConfig(AppConfig):
    """Клас `DailyHoroscopeConfig` інкапсулює повʼязану логіку проєкту.

    Базові класи: `AppConfig`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "daily_horoscope"
