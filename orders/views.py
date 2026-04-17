from __future__ import annotations

import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.permissions import support_required
from accounts.selectors import patient_users_queryset, is_patient
from analysis.models import Analysis

from .forms import (
    AuthenticatedOrderForm,
    GuestOrderForm,
    OrderCancelForm,
    SupportOrderCreateForm,
    SupportOrderUpdateForm,
)
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

User = get_user_model()


def _get_cart(request: HttpRequest) -> dict[str, int]:
    return request.session.get("cart", {})


def _clear_cart(request: HttpRequest) -> None:
    request.session["cart"] = {}
    request.session.modified = True


@transaction.atomic
def order_create_view(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        messages.warning(request, "Некоректний спосіб запиту.")
        return redirect("analysis:cart_detail")

    cart: dict[str, int] = _get_cart(request)

    if not cart:
        messages.warning(request, "Кошик порожній.")
        return redirect("analysis:cart_detail")

    form: GuestOrderForm | AuthenticatedOrderForm = get_order_form(request)

    if not form.is_valid():
        messages.warning(request, "Перевірте правильність заповнення форми.")
        return redirect("analysis:cart_detail")

    analysis_ids: list[int] = [int(item_id) for item_id in cart.keys()]
    analyses: QuerySet[Analysis] = Analysis.objects.filter(id__in=analysis_ids, is_active=True)

    if not analyses.exists():
        messages.warning(request, "Не вдалося оформити замовлення.")
        return redirect("analysis:cart_detail")

    payment_method: str = form.cleaned_data["payment_method"]
    total_price: Decimal = sum((analysis.price for analysis in analyses), Decimal("0.00"))

    if request.user.is_authenticated:
        user = request.user

        last_name = user.last_name
        first_name = user.first_name
        middle_name = user.middle_name

        phone = getattr(user, "phone", "") or ""
        email = user.email or ""
    else:
        user = None

        last_name = form.cleaned_data["last_name"]
        first_name = form.cleaned_data["first_name"]
        middle_name = form.cleaned_data.get("middle_name", "")

        phone = form.cleaned_data["phone"]
        email = form.cleaned_data["email"]

    order: Order = Order.objects.create(
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

    order_items: list[OrderItem] = [
        OrderItem(order=order, analysis=analysis, price=analysis.price)
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
    orders: QuerySet[Order] = Order.objects.filter(user=request.user).order_by("-created_at")
    update_bank_transfer_orders_status(orders)

    return render(
        request,
        "avelon_healthcare/orders/order_list.html",
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
        "avelon_healthcare/orders/order_detail.html",
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
        "avelon_healthcare/orders/order_cancel.html",
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


@login_required
@support_required
def support_order_list_view(request: HttpRequest) -> HttpResponse:
    orders = (
        Order.objects.prefetch_related("items__analysis")
        .select_related("user")
        .filter(
            Q(user__isnull=True) | Q(user__in=patient_users_queryset())
        )
        .distinct()
        .order_by("-created_at")
    )

    return render(
        request,
        "avelon_healthcare/orders/support_order_list.html",
        {"orders": orders},
    )


@login_required
@support_required
@transaction.atomic
def support_order_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SupportOrderCreateForm(request.POST)

        if form.is_valid():
            user: User | None = form.cleaned_data.get("user")

            if user and not is_patient(user):
                messages.error(request, "Можна обирати тільки користувачів із групою patient.")
                return redirect("orders:support_order_create")

            analyses = form.cleaned_data["analyses"]
            payment_method: str = form.cleaned_data["payment_method"]
            total_price: Decimal = sum((a.price for a in analyses), Decimal("0.00"))

            if user:
                last_name = user.last_name
                first_name = user.first_name
                middle_name = user.middle_name

                phone = getattr(user, "phone", "") or ""
                email = user.email or ""
            else:
                last_name = form.cleaned_data["last_name"]
                first_name = form.cleaned_data["first_name"]
                middle_name = form.cleaned_data.get("middle_name", "")

                phone = form.cleaned_data["phone"]
                email = form.cleaned_data["email"]

            order: Order = Order.objects.create(
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
                    OrderItem(order=order, analysis=a, price=a.price)
                    for a in analyses
                ]
            )

            return redirect("orders:support_order_list")
    else:
        form = SupportOrderCreateForm()

    return render(
        request,
        "avelon_healthcare/orders/support_order_form.html",
        {"form": form},
    )


@login_required
@support_required
def support_order_update_view(request: HttpRequest, order_id: int) -> HttpResponse:
    order: Order = get_object_or_404(
        Order.objects.prefetch_related("items__analysis").select_related("user"),
        Q(id=order_id) & (
            Q(user__isnull=True) | Q(user__in=patient_users_queryset())
        ),
    )

    if request.method == "POST":
        form = SupportOrderUpdateForm(request.POST, request.FILES, instance=order)

        if form.is_valid():
            updated_order: Order = form.save(commit=False)

            if updated_order.status == OrderStatus.PAID and updated_order.paid_at is None:
                updated_order.paid_at = timezone.now()

            if updated_order.status != OrderStatus.PAID:
                updated_order.paid_at = None

            if updated_order.status != OrderStatus.REJECTED:
                updated_order.rejection_reason = ""

            updated_order.save()
            return redirect("orders:support_order_list")
    else:
        form = SupportOrderUpdateForm(instance=order)

    return render(
        request,
        "avelon_healthcare/orders/support_order_update.html",
        {
            "form": form,
            "order": order,
        },
    )