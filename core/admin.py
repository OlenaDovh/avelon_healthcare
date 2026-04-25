from __future__ import annotations
from django.contrib import admin
from .models import ClinicInfo, ContactInfo, Promotion


@admin.register(ClinicInfo)
class ClinicInfoAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для сторінки "Про клініку".

    Налаштовує відображення інформації про клініку в адмін-панелі.
    """

    list_display = ("title",)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для контактної інформації.

    Налаштовує відображення контактів у адмін-панелі.
    """

    list_display = ("address", "work_schedule", "phone_1", "email")


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для акцій.

    Налаштовує відображення, фільтрацію та пошук акцій.
    """

    list_display = ("title", "end_date", "created_at")
    list_filter = ("end_date",)
    search_fields = ("title", "description")
