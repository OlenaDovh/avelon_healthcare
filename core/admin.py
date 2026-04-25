"""Модуль `core/admin.py` застосунку `core`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.contrib import admin

from .models import ClinicInfo, ContactInfo, Promotion


@admin.register(ClinicInfo)
class ClinicInfoAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для сторінки "Про клініку".
    """

    list_display = ("title",)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для контактної інформації.
    """

    list_display = ("address", "work_schedule", "phone_1", "email")


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для акцій.
    """

    list_display = ("title", "end_date", "created_at")
    list_filter = ("end_date",)
    search_fields = ("title", "description")
