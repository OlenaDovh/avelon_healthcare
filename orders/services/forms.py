from __future__ import annotations
from django.http import HttpRequest
from orders.forms import AuthenticatedOrderForm, GuestOrderForm


def get_order_form(request: HttpRequest) -> GuestOrderForm | AuthenticatedOrderForm:
    """
    Повертає відповідну форму оформлення замовлення залежно від авторизації користувача.

    Args:
        request: HTTP-запит.

    Returns:
        GuestOrderForm | AuthenticatedOrderForm: Форма замовлення.
    """
    if request.user.is_authenticated:
        return AuthenticatedOrderForm(request.POST or None)
    return GuestOrderForm(request.POST or None)
