from __future__ import annotations
from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone
from orders.models import Order, OrderStatus, PaymentMethod


def get_bank_transfer_auto_pay_after_minutes() -> int:
    """
    Повертає кількість хвилин, після яких замовлення з оплатою
    банківським переказом автоматично вважається оплаченим.

    Returns:
        int: Кількість хвилин (мінімум 1).
    """
    value = int(getattr(settings, "BANK_TRANSFER_AUTO_PAY_AFTER_MINUTES", 5))
    return max(value, 1)


def update_bank_transfer_order_status(order: Order) -> None:
    """
    Оновлює статус одного замовлення з типом оплати BANK_TRANSFER.

    Якщо з моменту створення замовлення пройшло достатньо часу —
    встановлює статус PAID.

    Args:
        order: Замовлення.

    Returns:
        None
    """
    if order.status != OrderStatus.NEW:
        return

    if order.payment_method != PaymentMethod.BANK_TRANSFER:
        return

    auto_pay_after_minutes = get_bank_transfer_auto_pay_after_minutes()
    paid_at_threshold = order.created_at + timezone.timedelta(minutes=auto_pay_after_minutes)

    if timezone.now() >= paid_at_threshold:
        order.status = OrderStatus.PAID
        order.paid_at = timezone.now()
        order.save(update_fields=["status", "paid_at"])


def update_bank_transfer_orders_status(orders: QuerySet[Order]) -> None:
    """
    Оновлює статуси списку замовлень.

    Args:
        orders: QuerySet замовлень.

    Returns:
        None
    """
    for order in orders:
        update_bank_transfer_order_status(order)