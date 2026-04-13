from __future__ import annotations

import logging
from decimal import Decimal

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from orders.forms import AuthenticatedOrderForm, GuestOrderForm

from .models import Analysis

logger = logging.getLogger(__name__)


def _get_cart(request: HttpRequest) -> dict[str, int]:
    """
    Повертає кошик із сесії.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        dict[str, int]: Словник з id аналізів та їх кількістю.
    """
    return request.session.setdefault("cart", {})


def _save_cart(request: HttpRequest, cart: dict[str, int]) -> None:
    """
    Зберігає кошик у сесії.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        cart (dict[str, int]): Поточний кошик.

    Returns:
        None
    """
    request.session["cart"] = cart
    request.session.modified = True


def analysis_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список аналізів з фільтрами.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі списком аналізів.
    """
    what_to_check: str = request.GET.get("what_to_check", "").strip()
    disease: str = request.GET.get("disease", "").strip()
    for_whom: str = request.GET.get("for_whom", "").strip()
    biomaterial: str = request.GET.get("biomaterial", "").strip()

    analyses: QuerySet[Analysis] = Analysis.objects.filter(is_active=True)

    if what_to_check:
        analyses = analyses.filter(what_to_check__icontains=what_to_check)

    if disease:
        analyses = analyses.filter(disease__icontains=disease)

    if for_whom:
        analyses = analyses.filter(for_whom__icontains=for_whom)

    if biomaterial:
        analyses = analyses.filter(biomaterial__icontains=biomaterial)

    cart: dict[str, int] = _get_cart(request)

    what_to_check_values = (
        Analysis.objects.exclude(what_to_check="")
        .values_list("what_to_check", flat=True)
        .distinct()
        .order_by("what_to_check")
    )
    disease_values = (
        Analysis.objects.exclude(disease="")
        .values_list("disease", flat=True)
        .distinct()
        .order_by("disease")
    )
    for_whom_values = (
        Analysis.objects.exclude(for_whom="")
        .values_list("for_whom", flat=True)
        .distinct()
        .order_by("for_whom")
    )
    biomaterial_values = (
        Analysis.objects.exclude(biomaterial="")
        .values_list("biomaterial", flat=True)
        .distinct()
        .order_by("biomaterial")
    )

    logger.info("Відкрито сторінку списку аналізів.")

    return render(
        request,
        "avelon_healthcare/analysis/analysis_list.html",
        {
            "analyses": analyses,
            "cart": cart,
            "what_to_check_values": what_to_check_values,
            "disease_values": disease_values,
            "for_whom_values": for_whom_values,
            "biomaterial_values": biomaterial_values,
            "selected_what_to_check": what_to_check,
            "selected_disease": disease,
            "selected_for_whom": for_whom,
            "selected_biomaterial": biomaterial,
        },
    )


def add_to_cart_view(request: HttpRequest, analysis_id: int) -> HttpResponse:
    """
    Додає аналіз до кошика в сесії.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        analysis_id (int): Ідентифікатор аналізу.

    Returns:
        HttpResponse: Редірект на сторінку аналізів.
    """
    analysis: Analysis = get_object_or_404(Analysis, id=analysis_id, is_active=True)
    cart: dict[str, int] = _get_cart(request)

    cart[str(analysis.id)] = 1
    _save_cart(request, cart)

    logger.info("Додано аналіз до кошика. analysis_id=%s", analysis.id)

    return redirect("analysis:analysis_list")


def remove_from_cart_view(request: HttpRequest, analysis_id: int) -> HttpResponse:
    """
    Видаляє аналіз із кошика в сесії.

    Args:
        request (HttpRequest): HTTP-запит користувача.
        analysis_id (int): Ідентифікатор аналізу.

    Returns:
        HttpResponse: Редірект на сторінку аналізів або кошика.
    """
    cart: dict[str, int] = _get_cart(request)
    cart.pop(str(analysis_id), None)
    _save_cart(request, cart)

    logger.info("Видалено аналіз із кошика. analysis_id=%s", analysis_id)

    next_url: str = request.GET.get("next", "analysis:analysis_list")
    return redirect(next_url)


def cart_detail_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає сторінку кошика з аналізами.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою кошика.
    """
    cart: dict[str, int] = _get_cart(request)
    analysis_ids: list[int] = [int(item_id) for item_id in cart.keys()]

    analyses: QuerySet[Analysis] = Analysis.objects.filter(id__in=analysis_ids)
    total_price: Decimal = sum((analysis.price for analysis in analyses), Decimal("0.00"))

    recommended_analyses: QuerySet[Analysis] = Analysis.objects.filter(is_active=True).exclude(
        id__in=analysis_ids
    )[:3]

    logger.info("Відкрито сторінку кошика.")

    order_form: GuestOrderForm | AuthenticatedOrderForm
    if request.user.is_authenticated:
        order_form = AuthenticatedOrderForm()
    else:
        order_form = GuestOrderForm()

    return render(
        request,
        "avelon_healthcare/analysis/cart_detail.html",
        {
            "analyses": analyses,
            "total_price": total_price,
            "recommended_analyses": recommended_analyses,
            "order_form": order_form,
        },
    )