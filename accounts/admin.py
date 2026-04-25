"""Модуль `accounts/admin.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Клас `CustomUserAdmin` інкапсулює повʼязану логіку проєкту.

    Базові класи: `UserAdmin`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ("Додаткові поля", {
            "fields": (
                "phone",
                "pending_email",
                "email_verified",
                "discount",
                "birth_date",
                "preferred_contact_channel",
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Додаткові поля", {
            "fields": ("email", "phone"),
        }),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "middle_name",
        "phone",
        "email",
        "pending_email",
        "is_staff",
        "email_verified",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "email_verified",
    )

    search_fields = ("username", "email", "phone", "pending_email")

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        """Виконує прикладну логіку функції `save_model` у відповідному модулі проєкту.

        Параметри:
            request: Значення типу `Any`, яке передається для виконання логіки функції.
            obj: Значення типу `Any`, яке передається для виконання логіки функції.
            form: Значення типу `Any`, яке передається для виконання логіки функції.
            change: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            None: Функція виконує дію без явного значення результату.
        """
        if obj.email:
            obj.email_verified = True
            obj.pending_email = ""

        super().save_model(request, obj, form, change)
