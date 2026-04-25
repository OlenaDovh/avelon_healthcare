"""Модуль `reviews/admin.py` застосунку `reviews`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для моделі відгуку.
    """

    list_display = (
        "user",
        "appointment",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__email",
        "text",
        "clinic_reply",
    )
    readonly_fields = ("created_at",)
    fields = (
        "user",
        "appointment",
        "text",
        "clinic_reply",
        "created_at",
    )
