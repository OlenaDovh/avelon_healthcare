from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from orders.forms import OrderCancelForm
from orders.models import Order, OrderStatus, PaymentMethod
from orders.services import (
    build_order_invoice_response,
    get_bank_transfer_auto_pay_after_minutes,
    update_bank_transfer_order_status,
    update_bank_transfer_orders_status,
)


@login_required
def order_list_view(request: HttpRequest) -> HttpResponse:
    orders: QuerySet[Order] = Order.objects.filter(user=request.user).order_by("-created_at")
    update_bank_transfer_orders_status(orders)

    return render(
        request,
        "avelon_healthcare/orders/pages/order_list.html",
        {"orders": orders},
    )


@login_required
def order_detail_view(request: HttpRequest, order_id: int) -> HttpResponse:
    order: Order = get_object_or_404(
        Order.objects.prefetch_related("items__analysis"),
        id=order_id,
        user=request.user,
    )

    update_bank_transfer_order_status(order)

    return render(
        request,
        "avelon_healthcare/orders/pages/order_detail.html",
        {
            "order": order,
            "bank_transfer_auto_pay_after_minutes": get_bank_transfer_auto_pay_after_minutes(),
        },
    )


@login_required
@transaction.atomic
def order_pay_view(request: HttpRequest, order_id: int) -> HttpResponse:
    order: Order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method != "POST":
        return redirect("orders:order_detail", order_id=order.id)

    if order.status != OrderStatus.NEW:
        return redirect("orders:order_detail", order_id=order.id)

    if order.payment_method != PaymentMethod.ONLINE:
        return redirect("orders:order_detail", order_id=order.id)

    order.status = OrderStatus.PAID
    order.paid_at = timezone.now()
    order.save(update_fields=["status", "paid_at"])

    return redirect("orders:order_detail", order_id=order.id)


@login_required
def order_cancel_view(request: HttpRequest, order_id: int) -> HttpResponse:
    order: Order = get_object_or_404(
        Order.objects.select_related("user"),
        pk=order_id,
        user=request.user,
    )

    if order.status != OrderStatus.NEW:
        return redirect("orders:order_list")

    if request.method == "POST":
        form = OrderCancelForm(request.POST)

        if form.is_valid():
            user_reason: str = form.cleaned_data["reason"]

            order.status = OrderStatus.REJECTED
            order.rejection_reason = user_reason
            order.save(update_fields=["status", "rejection_reason"])

            return redirect("orders:order_list")
    else:
        form = OrderCancelForm()

    return render(
        request,
        "avelon_healthcare/orders/pages/order_cancel.html",
        {
            "order": order,
            "form": form,
        },
    )


@login_required
def order_invoice_view(request: HttpRequest, order_id: int) -> HttpResponse:
    order: Order = get_object_or_404(
        Order.objects.prefetch_related("items__analysis"),
        id=order_id,
        user=request.user,
    )

    if order.payment_method != PaymentMethod.BANK_TRANSFER:
        return redirect("orders:order_detail", order_id=order.id)

    return build_order_invoice_response(order)