from __future__ import annotations

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.permissions import support_required
from accounts.selectors import is_patient, patient_users_queryset
from orders.forms import SupportOrderCreateForm, SupportOrderUpdateForm
from orders.models import Order, OrderItem, OrderStatus

User = get_user_model()


@login_required
@support_required
def support_order_list_view(request: HttpRequest) -> HttpResponse:
    orders = (
        Order.objects.prefetch_related("items__analysis")
        .select_related("user")
        .filter(Q(user__isnull=True) | Q(user__in=patient_users_queryset()))
        .distinct()
        .order_by("-created_at")
    )

    return render(
        request,
        "avelon_healthcare/orders/pages/support_order_list.html",
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
        "avelon_healthcare/orders/pages/support_order_form.html",
        {"form": form},
    )


@login_required
@support_required
def support_order_update_view(request: HttpRequest, order_id: int) -> HttpResponse:
    order: Order = get_object_or_404(
        Order.objects.prefetch_related("items__analysis").select_related("user"),
        Q(id=order_id) & (Q(user__isnull=True) | Q(user__in=patient_users_queryset())),
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
        "avelon_healthcare/orders/pages/support_order_update.html",
        {
            "form": form,
            "order": order,
        },
    )