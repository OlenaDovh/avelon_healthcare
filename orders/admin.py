"""Модуль orders/admin.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
from django.contrib import admin
from django.utils import timezone
from .models import Order, OrderItem, OrderStatus

class OrderItemInline(admin.TabularInline):
    """Клас OrderItemInline.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    model = OrderItem
    extra = 0
    readonly_fields = ('analysis', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Клас OrderAdmin.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    list_display = ('id', 'user', 'full_name', 'phone', 'email', 'status', 'payment_method', 'total_price', 'paid_at', 'created_at', 'rejection_reason')
    list_filter = ('status', 'payment_method', 'created_at', 'paid_at')
    search_fields = ('user__username', 'user__email', 'full_name', 'phone', 'email')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]
    fields = ('user', 'full_name', 'phone', 'email', 'status', 'rejection_reason', 'payment_method', 'paid_at', 'total_price', 'result_file', 'created_at')

    def save_model(self, request: Any, obj: Order, form: Any, change: bool) -> None:
        """Виконує логіку `save_model`.

Args:
    request: Вхідне значення для виконання операції.
    obj: Вхідне значення для виконання операції.
    form: Вхідне значення для виконання операції.
    change: Вхідне значення для виконання операції.

Returns:
    None."""
        if obj.status == OrderStatus.PAID and obj.paid_at is None:
            obj.paid_at = timezone.now()
        if obj.status != OrderStatus.PAID:
            obj.paid_at = None
        if obj.status != OrderStatus.REJECTED:
            obj.rejection_reason = ''
        super().save_model(request, obj, form, change)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Клас OrderItemAdmin.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    list_display = ('order', 'analysis', 'price')
    search_fields = ('order__id', 'analysis__name')
