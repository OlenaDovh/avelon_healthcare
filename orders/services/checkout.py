"""Модуль orders/services/checkout.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
from decimal import Decimal
from django.db.models import QuerySet
from analysis.models import Analysis
from orders.models import Order, OrderItem, OrderStatus

def create_order_from_analyses(*, analyses: QuerySet[Analysis], payment_method: str, user: Any=None, last_name: str='', first_name: str='', middle_name: str='', phone: str='', email: str='') -> Order:
    """Виконує логіку `create_order_from_analyses`.

Args:
    analyses: Вхідне значення для виконання операції.
    payment_method: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.
    last_name: Вхідне значення для виконання операції.
    first_name: Вхідне значення для виконання операції.
    middle_name: Вхідне значення для виконання операції.
    phone: Вхідне значення для виконання операції.
    email: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    total_price: Decimal = sum((analysis.price for analysis in analyses), Decimal('0.00'))
    order = Order.objects.create(user=user, last_name=last_name, first_name=first_name, middle_name=middle_name, phone=phone, email=email, total_price=total_price, payment_method=payment_method, status=OrderStatus.NEW)
    OrderItem.objects.bulk_create([OrderItem(order=order, analysis=analysis, price=analysis.price) for analysis in analyses])
    return order
