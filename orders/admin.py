from __future__ import annotations

from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline-форма для елементів замовлення в адмінці.
    """

    model = OrderItem
    extra = 0
    readonly_fields = ("analysis", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для моделі замовлення.
    """

    list_display = (
        "id",
        "user",
        "status",
        "total_price",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Адмін-інтерфейс для моделі елемента замовлення.
    """

    list_display = ("order", "analysis", "price")
    search_fields = ("order__id", "analysis__name")