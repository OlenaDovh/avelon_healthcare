"""Модуль `orders/services/payments.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone

from orders.models import Order, OrderStatus, PaymentMethod


def get_bank_transfer_auto_pay_after_minutes() -> int:
    """Виконує прикладну логіку функції `get_bank_transfer_auto_pay_after_minutes` у відповідному модулі проєкту.

    Повертає:
        int: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    value = int(getattr(settings, "BANK_TRANSFER_AUTO_PAY_AFTER_MINUTES", 5))
    return max(value, 1)


def update_bank_transfer_order_status(order: Order) -> None:
    """Виконує прикладну логіку функції `update_bank_transfer_order_status` у відповідному модулі проєкту.

    Параметри:
        order: Значення типу `Order`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
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
    """Виконує прикладну логіку функції `update_bank_transfer_orders_status` у відповідному модулі проєкту.

    Параметри:
        orders: Значення типу `QuerySet[Order]`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    for order in orders:
        update_bank_transfer_order_status(order)
