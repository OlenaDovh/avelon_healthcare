from __future__ import annotations

from decimal import Decimal

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from analysis.models import Analysis
from analysis.selectors import analysis_filter_values, filtered_analyses_queryset
from analysis.services.cart import add_analysis_to_cart, get_cart, remove_analysis_from_cart
from orders.forms import AuthenticatedOrderForm, GuestOrderForm


def analysis_list_view(request: HttpRequest) -> HttpResponse:
    what_to_check = request.GET.get("what_to_check", "").strip()
    disease = request.GET.get("disease", "").strip()
    for_whom = request.GET.get("for_whom", "").strip()
    biomaterial = request.GET.get("biomaterial", "").strip()

    analyses = filtered_analyses_queryset(
        what_to_check=what_to_check,
        disease=disease,
        for_whom=for_whom,
        biomaterial=biomaterial,
    )

    cart = get_cart(request)
    filters_data = analysis_filter_values()

    return render(
        request,
        "avelon_healthcare/analysis/pages/analysis_list.html",
        {
            "analyses": analyses,
            "cart": cart,
            **filters_data,
            "selected_what_to_check": what_to_check,
            "selected_disease": disease,
            "selected_for_whom": for_whom,
            "selected_biomaterial": biomaterial,
        },
    )


def add_to_cart_view(request: HttpRequest, analysis_id: int) -> HttpResponse:
    analysis = get_object_or_404(Analysis, id=analysis_id, is_active=True)
    add_analysis_to_cart(request, analysis.id)
    return redirect("analysis:analysis_list")


def remove_from_cart_view(request: HttpRequest, analysis_id: int) -> HttpResponse:
    remove_analysis_from_cart(request, analysis_id)
    next_url = request.GET.get("next", "analysis:analysis_list")
    return redirect(next_url)


def cart_detail_view(request: HttpRequest) -> HttpResponse:
    cart = get_cart(request)
    analysis_ids = [int(item_id) for item_id in cart.keys()]
    analyses: QuerySet[Analysis] = Analysis.objects.filter(id__in=analysis_ids)
    total_price: Decimal = sum((analysis.price for analysis in analyses), Decimal("0.00"))

    recommended_analyses = Analysis.objects.filter(is_active=True).exclude(id__in=analysis_ids)[:3]
    order_form = AuthenticatedOrderForm() if request.user.is_authenticated else GuestOrderForm()

    return render(
        request,
        "avelon_healthcare/analysis/pages/cart_detail.html",
        {
            "analyses": analyses,
            "total_price": total_price,
            "recommended_analyses": recommended_analyses,
            "order_form": order_form,
        },
    )