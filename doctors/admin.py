from __future__ import annotations

from django.contrib import admin

from .models import Direction, Doctor


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для моделі напряму.
    """

    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для моделі лікаря.
    """

    list_display = (
        "full_name",
        "position",
        "specialty_name",
        "qualification_category",
        "experience_years",
        "price_from",
        "price_to",
    )
    search_fields = ("full_name", "position", "specialty_name")
    list_filter = ("position", "qualification_category", "directions")
    filter_horizontal = ("directions",)