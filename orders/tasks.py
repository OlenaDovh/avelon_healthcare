"""Модуль orders/tasks.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from celery import shared_task
from orders.models import Order
from orders.services.notifications import send_order_email

@shared_task
def send_order_email_task(order_id: int) -> None:
    """Виконує логіку `send_order_email_task`.

Args:
    order_id: Вхідне значення для виконання операції.

Returns:
    None."""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return
    send_order_email(order)
