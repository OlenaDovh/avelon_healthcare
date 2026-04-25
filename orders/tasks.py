"""Модуль `orders/tasks.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from celery import shared_task

from orders.models import Order
from orders.services.notifications import send_order_email


@shared_task
def send_order_email_task(order_id: int) -> None:
    """Виконує прикладну логіку функції `send_order_email_task` у відповідному модулі проєкту.

    Параметри:
        order_id: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    send_order_email(order)
