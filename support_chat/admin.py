"""Модуль `support_chat/admin.py` застосунку `support_chat`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from django.contrib import admin

from .models import SupportChatMessage, SupportChatSession


class SupportChatMessageInline(admin.TabularInline):
    """Клас `SupportChatMessageInline` інкапсулює повʼязану логіку проєкту.

    Базові класи: `admin.TabularInline`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    model = SupportChatMessage
    extra = 0
    readonly_fields = ("author_type", "author_name", "text", "created_at")
    can_delete = False


@admin.register(SupportChatSession)
class SupportChatSessionAdmin(admin.ModelAdmin):
    """Клас `SupportChatSessionAdmin` інкапсулює повʼязану логіку проєкту.

    Базові класи: `admin.ModelAdmin`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    list_display = (
        "id",
        "customer_display_name",
        "topic",
        "status",
        "operator",
        "created_at",
    )
    list_filter = ("status", "topic", "created_at")
    search_fields = ("guest_name", "guest_email", "user__username", "user__email")
    readonly_fields = ("created_at", "connected_at", "closed_at")
    inlines = [SupportChatMessageInline]
