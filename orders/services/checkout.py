from __future__ import annotations

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