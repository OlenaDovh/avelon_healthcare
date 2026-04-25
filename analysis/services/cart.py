from __future__ import annotations
from django.http import HttpRequest

def get_cart(request: HttpRequest) -> dict[str, int]:
    """Виконує логіку `get_cart`.

Args:
    request: Вхідний параметр `request`.

Returns:
    Any: Результат виконання."""
    return request.session.setdefault('cart', {})

def save_cart(request: HttpRequest, cart: dict[str, int]) -> None:
    """Виконує логіку `save_cart`.

Args:
    request: Вхідний параметр `request`.
    cart: Вхідний параметр `cart`.

Returns:
    Any: Результат виконання."""
    request.session['cart'] = cart
    request.session.modified = True

def add_analysis_to_cart(request: HttpRequest, analysis_id: int) -> None:
    """Виконує логіку `add_analysis_to_cart`.

Args:
    request: Вхідний параметр `request`.
    analysis_id: Вхідний параметр `analysis_id`.

Returns:
    Any: Результат виконання."""
    cart = get_cart(request)
    cart[str(analysis_id)] = 1
    save_cart(request, cart)

def remove_analysis_from_cart(request: HttpRequest, analysis_id: int) -> None:
    """Виконує логіку `remove_analysis_from_cart`.

Args:
    request: Вхідний параметр `request`.
    analysis_id: Вхідний параметр `analysis_id`.

Returns:
    Any: Результат виконання."""
    cart = get_cart(request)
    cart.pop(str(analysis_id), None)
    save_cart(request, cart)
