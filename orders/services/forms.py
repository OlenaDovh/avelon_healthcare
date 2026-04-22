from __future__ import annotations

from django.http import HttpRequest

from orders.forms import AuthenticatedOrderForm, GuestOrderForm


def get_order_form(request: HttpRequest) -> GuestOrderForm | AuthenticatedOrderForm:
    if request.user.is_authenticated:
        return AuthenticatedOrderForm(request.POST or None)
    return GuestOrderForm(request.POST or None)