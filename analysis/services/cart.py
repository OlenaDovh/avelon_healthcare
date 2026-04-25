"""Модуль analysis/services/cart.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.http import HttpRequest

def get_cart(request: HttpRequest) -> dict[str, int]:
    """Виконує логіку `get_cart`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    return request.session.setdefault('cart', {})

def save_cart(request: HttpRequest, cart: dict[str, int]) -> None:
    """Виконує логіку `save_cart`.

Args:
    request: Вхідне значення для виконання операції.
    cart: Вхідне значення для виконання операції.

Returns:
    None."""
    request.session['cart'] = cart
    request.session.modified = True

def add_analysis_to_cart(request: HttpRequest, analysis_id: int) -> None:
    """Виконує логіку `add_analysis_to_cart`.

Args:
    request: Вхідне значення для виконання операції.
    analysis_id: Вхідне значення для виконання операції.

Returns:
    None."""
    cart = get_cart(request)
    cart[str(analysis_id)] = 1
    save_cart(request, cart)

def remove_analysis_from_cart(request: HttpRequest, analysis_id: int) -> None:
    """Виконує логіку `remove_analysis_from_cart`.

Args:
    request: Вхідне значення для виконання операції.
    analysis_id: Вхідне значення для виконання операції.

Returns:
    None."""
    cart = get_cart(request)
    cart.pop(str(analysis_id), None)
    save_cart(request, cart)
