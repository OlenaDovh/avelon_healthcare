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