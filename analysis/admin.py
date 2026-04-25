"""Модуль `analysis/admin.py` застосунку `analysis`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.contrib import admin

from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для моделі аналізу.
    """

    list_display = (
        "name",
        "what_to_check",
        "disease",
        "for_whom",
        "biomaterial",
        "duration_days",
        "price",
        "is_active",
    )
    list_filter = ("what_to_check", "disease", "for_whom", "biomaterial", "is_active")
    search_fields = ("name", "what_to_check", "disease", "for_whom", "biomaterial")
