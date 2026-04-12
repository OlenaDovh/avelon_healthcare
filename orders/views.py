from __future__ import annotations

import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from analysis.models import Analysis

from .forms import AuthenticatedOrderForm, GuestOrderForm
from .models import Order, OrderItem, OrderStatus, PaymentMethod
from .utils import (
    build_order_invoice_response,
    get_bank_transfer_auto_pay_after_minutes,
    get_order_form,
    send_order_email,
    update_bank_transfer_order_status,
    update_bank_transfer_orders_status,
)

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


@transaction.atomic
def order_create_view(request: HttpRequest) -> HttpResponse:
    """
    Створює замовлення на основі вмісту кошика.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: Редірект на сторінку деталей замовлення або кошика.
    """
    if request.method != "POST":
        messages.warning(request, "Некоректний спосіб запиту.")
        return redirect("analysis:cart_detail")

    cart: dict[str, int] = _get_cart(request)

    if not cart:
        logger.warning("Спроба оформити порожній кошик.")
        messages.warning(request, "Кошик порожній.")
        return redirect("analysis:cart_detail")

    form: GuestOrderForm | AuthenticatedOrderForm = get_order_form(request)

    if not form.is_valid():
        messages.warning(request, "Перевірте правильність заповнення форми.")
        return redirect("analysis:cart_detail")

    analysis_ids: list[int] = [int(item_id) for item_id in cart.keys()]
    analyses: QuerySet[Analysis] = Analysis.objects.filter(id__in=analysis_ids, is_active=True)

    if not analyses.exists():
        logger.warning("Спроба оформити замовлення без валідних аналізів.")
        messages.warning(request, "Не вдалося оформити замовлення.")
        return redirect("analysis:cart_detail")

    payment_method: str = form.cleaned_data["payment_method"]
    total_price: Decimal = sum((analysis.price for analysis in analyses), Decimal("0.00"))

    if request.user.is_authenticated:
        full_name: str = request.user.get_full_name() or request.user.username
        phone: str = getattr(request.user, "phone", "") or ""
        email: str = request.user.email or ""
        user = request.user
    else:
        full_name = form.cleaned_data["full_name"]
        phone = form.cleaned_data["phone"]
        email = form.cleaned_data["email"]
        user = None

    order: Order = Order.objects.create(
        user=user,
        full_name=full_name,
        phone=phone,
        email=email,
        total_price=total_price,
        payment_method=payment_method,
        status=OrderStatus.NEW,
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

    send_order_email(order)
    _clear_cart(request)

    messages.success(request, "Замовлення аналізів успішно оформлено.")

    if request.user.is_authenticated:
        return redirect("orders:order_detail", order_id=order.id)

    return redirect("core:home")


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
    update_bank_transfer_orders_status(orders)

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

    update_bank_transfer_order_status(order)

    return render(
        request,
        "avelon_healthcare/orders/order_detail.html",
        {
            "order": order,
            "bank_transfer_auto_pay_after_minutes": get_bank_transfer_auto_pay_after_minutes(),
        },
    )


@login_required
@transaction.atomic
def order_pay_view(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Проводить мок-оплату онлайн для замовлення.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        order_id (int): Ідентифікатор замовлення.

    Returns:
        HttpResponse: Редірект на сторінку деталей замовлення.
    """
    order: Order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    if request.method != "POST":
        messages.warning(request, "Некоректний спосіб запиту.")
        return redirect("orders:order_detail", order_id=order.id)

    if order.status != OrderStatus.NEW:
        messages.warning(request, "Оплата доступна лише для нового замовлення.")
        return redirect("orders:order_detail", order_id=order.id)

    if order.payment_method != PaymentMethod.ONLINE:
        messages.warning(request, "Для цього замовлення онлайн-оплата недоступна.")
        return redirect("orders:order_detail", order_id=order.id)

    payment_provider: str = request.POST.get("payment_provider", "").strip()

    valid_payment_providers: set[str] = {
        "portmone",
        "easypay",
        "ipay",
        "masterpass",
    }
    if payment_provider not in valid_payment_providers:
        messages.warning(request, "Оберіть платіжну систему.")
        return redirect("orders:order_detail", order_id=order.id)

    order.status = OrderStatus.PAID
    order.paid_at = timezone.now()
    order.save(update_fields=["status", "paid_at"])

    logger.info(
        "Виконано онлайн-оплату замовлення. user=%s order_id=%s provider=%s",
        request.user.username,
        order.id,
        payment_provider,
    )

    messages.success(request, "Оплату успішно проведено.")
    return redirect("orders:order_detail", order_id=order.id)


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


@login_required
def order_invoice_view(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Генерує PDF-рахунок для замовлення.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        order_id (int): Ідентифікатор замовлення.

    Returns:
        HttpResponse: PDF-файл із рахунком.
    """
    order: Order = get_object_or_404(
        Order.objects.prefetch_related("items__analysis"),
        id=order_id,
        user=request.user,
    )

    if order.payment_method != PaymentMethod.BANK_TRANSFER:
        messages.warning(request, "Рахунок доступний лише для оплати на рахунок.")
        return redirect("orders:order_detail", order_id=order.id)

    return build_order_invoice_response(order)