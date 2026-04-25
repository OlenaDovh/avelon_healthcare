from __future__ import annotations

from django.http import HttpRequest


def cart_items_count(request: HttpRequest) -> dict[str, int]:
    """
    Повертає кількість елементів кошика для контексту шаблонів.

    Args:
        request: HTTP-запит.

    Returns:
        dict[str, int]: Словник з кількістю елементів кошика.
    """
    cart = request.session.get("cart", {})
    return {
        "cart_items_count": len(cart),
    }
