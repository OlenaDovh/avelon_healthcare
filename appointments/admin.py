from __future__ import annotations

from django.contrib import admin

from .models import Appointment, AppointmentStatus


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для моделі запису до лікаря.
    """

    list_display = (
        "user",
        "full_name",
        "phone",
        "email",
        "direction",
        "doctor",
        "appointment_date",
        "appointment_time",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "direction",
        "appointment_date",
    )
    search_fields = (
        "user__username",
        "user__email",
        "full_name",
        "phone",
        "email",
        "doctor__full_name",
        "direction__name",
    )
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Основна інформація",
            {
                "fields": (
                    "user",
                    "full_name",
                    "phone",
                    "email",
                    "direction",
                    "doctor",
                    "appointment_date",
                    "appointment_time",
                    "description",
                    "status",
                )
            },
        ),
        (
            "Документи",
            {
                "fields": ("final_conclusion",),
            },
        ),
        (
            "Системна інформація",
            {
                "fields": ("created_at",),
            },
        ),
    )