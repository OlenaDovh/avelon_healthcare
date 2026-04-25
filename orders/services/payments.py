"""Модуль orders/services/payments.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone
from orders.models import Order, OrderStatus, PaymentMethod

def get_bank_transfer_auto_pay_after_minutes() -> int:
    """Виконує логіку `get_bank_transfer_auto_pay_after_minutes`.

Returns:
    Результат виконання операції."""
    value = int(getattr(settings, 'BANK_TRANSFER_AUTO_PAY_AFTER_MINUTES', 5))
    return max(value, 1)

def update_bank_transfer_order_status(order: Order) -> None:
    """Виконує логіку `update_bank_transfer_order_status`.

Args:
    order: Вхідне значення для виконання операції.

Returns:
    None."""
    if order.status != OrderStatus.NEW:
        return
    if order.payment_method != PaymentMethod.BANK_TRANSFER:
        return
    auto_pay_after_minutes = get_bank_transfer_auto_pay_after_minutes()
    paid_at_threshold = order.created_at + timezone.timedelta(minutes=auto_pay_after_minutes)
    if timezone.now() >= paid_at_threshold:
        order.status = OrderStatus.PAID
        order.paid_at = timezone.now()
        order.save(update_fields=['status', 'paid_at'])

def update_bank_transfer_orders_status(orders: QuerySet[Order]) -> None:
    """Виконує логіку `update_bank_transfer_orders_status`.

Args:
    orders: Вхідне значення для виконання операції.

Returns:
    None."""
    for order in orders:
        update_bank_transfer_order_status(order)
