from __future__ import annotations
from celery import shared_task
from orders.models import Order
from orders.services.notifications import send_order_email


@shared_task
def send_order_email_task(order_id: int) -> None:
    """
    Celery-задача для надсилання email про замовлення.

    Args:
        order_id: ID замовлення.

    Returns:
        None
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    send_order_email(order)
