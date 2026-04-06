from __future__ import annotations

import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from analysis.models import Analysis

from .models import Order, OrderItem, OrderStatus

logger = logging.getLogger(__name__)


def _get_cart(request: HttpRequest) -> dict[str, int]:
    """
    Повертає кошик із сесії.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        dict[str, int]: Поточний кошик.
    """
    return request.session.get("cart", {})


def _clear_cart(request: HttpRequest) -> None:
    """
    Очищає кошик у сесії.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        None
    """
    request.session["cart"] = {}
    request.session.modified = True


@login_required
@transaction.atomic
def order_create_view(request: HttpRequest) -> HttpResponse:
    """
    Створює замовлення на основі вмісту кошика.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: Редірект на список замовлень або сторінку кошика.
    """
    cart: dict[str, int] = _get_cart(request)

    if not cart:
        logger.warning(
            "Спроба оформити порожній кошик. user=%s",
            request.user.username,
        )
        messages.warning(request, "Кошик порожній.")
        return redirect("analysis:cart_detail")

    analysis_ids: list[int] = [int(item_id) for item_id in cart.keys()]
    analyses: QuerySet[Analysis] = Analysis.objects.filter(id__in=analysis_ids, is_active=True)

    if not analyses.exists():
        logger.warning(
            "Спроба оформити замовлення без валідних аналізів. user=%s",
            request.user.username,
        )
        messages.warning(request, "Не вдалося оформити замовлення.")
        return redirect("analysis:cart_detail")

    total_price: Decimal = sum((analysis.price for analysis in analyses), Decimal("0.00"))

    order: Order = Order.objects.create(
        user=request.user,
        total_price=total_price,
    )

    order_items: list[OrderItem] = [
        OrderItem(
            order=order,
            analysis=analysis,
            price=analysis.price,
        )
        for analysis in analyses
    ]
    OrderItem.objects.bulk_create(order_items)

    _clear_cart(request)

    logger.info(
        "Створено замовлення аналізів. user=%s order_id=%s total=%s",
        request.user.username,
        order.id,
        order.total_price,
    )

    messages.success(request, "Замовлення аналізів успішно оформлено.")
    return redirect("orders:order_list")


@login_required
def order_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список замовлень поточного користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі списком замовлень.
    """
    orders: QuerySet[Order] = Order.objects.filter(user=request.user).order_by("-created_at")

    logger.info("Відкрито список замовлень. user=%s", request.user.username)

    return render(
        request,
        "avelon_healthcare/orders/order_list.html",
        {"orders": orders},
    )


@login_required
def order_detail_view(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Відображає деталі замовлення поточного користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        order_id (int): Ідентифікатор замовлення.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою деталей замовлення.
    """
    order: Order = get_object_or_404(
        Order.objects.prefetch_related("items__analysis"),
        id=order_id,
        user=request.user,
    )

    logger.info(
        "Відкрито деталі замовлення. user=%s order_id=%s",
        request.user.username,
        order.id,
    )

    return render(
        request,
        "avelon_healthcare/orders/order_detail.html",
        {"order": order},
    )


@login_required
def order_cancel_view(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Скасовує замовлення поточного користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        order_id (int): Ідентифікатор замовлення.

    Returns:
        HttpResponse: Редірект на список замовлень.
    """
    order: Order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    if order.status == OrderStatus.NEW:
        order.status = OrderStatus.REJECTED
        order.save(update_fields=["status"])

        logger.info(
            "Скасовано замовлення. user=%s order_id=%s",
            request.user.username,
            order.id,
        )
        messages.success(request, "Замовлення успішно скасовано.")
    else:
        logger.warning(
            "Спроба скасувати замовлення з неактивним статусом. user=%s order_id=%s",
            request.user.username,
            order.id,
        )
        messages.warning(
            request,
            "Скасувати можна лише замовлення зі статусом 'Нове'.",
        )

    return redirect("orders:order_list")