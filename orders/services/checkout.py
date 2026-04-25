"""Модуль `orders/services/checkout.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations
from typing import Any

from decimal import Decimal
from django.db.models import QuerySet

from analysis.models import Analysis
from orders.models import Order, OrderItem, OrderStatus


def create_order_from_analyses(
    *,
    analyses: QuerySet[Analysis],
    payment_method: str,
    user=None,
    last_name: str = "",
    first_name: str = "",
    middle_name: str = "",
    phone: str = "",
    email: str = "",
) -> Order:
    """Виконує прикладну логіку функції `create_order_from_analyses` у відповідному модулі проєкту.

    Параметри:
        analyses: Значення типу `QuerySet[Analysis]`, яке передається для виконання логіки функції.
        payment_method: Значення типу `str`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        last_name: Значення типу `str`, яке передається для виконання логіки функції.
        first_name: Значення типу `str`, яке передається для виконання логіки функції.
        middle_name: Значення типу `str`, яке передається для виконання логіки функції.
        phone: Значення типу `str`, яке передається для виконання логіки функції.
        email: Значення типу `str`, яке передається для виконання логіки функції.

    Повертає:
        Order: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    total_price: Decimal = sum((analysis.price for analysis in analyses), Decimal("0.00"))

    order = Order.objects.create(
        user=user,
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        phone=phone,
        email=email,
        total_price=total_price,
        payment_method=payment_method,
        status=OrderStatus.NEW,
    )

    OrderItem.objects.bulk_create(
        [
            OrderItem(order=order, analysis=analysis, price=analysis.price)
            for analysis in analyses
        ]
    )

    return order
