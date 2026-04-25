"""Модуль analysis/context_processors.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.http import HttpRequest

def cart_items_count(request: HttpRequest) -> dict[str, int]:
    """Виконує логіку `cart_items_count`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    cart: dict[str, int] = request.session.get('cart', {})
    return {'cart_items_count': len(cart)}
