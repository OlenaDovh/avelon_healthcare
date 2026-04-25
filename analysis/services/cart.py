from __future__ import annotations
from django.http import HttpRequest


def get_cart(request: HttpRequest) -> dict[str, int]:
    """
    Повертає кошик користувача із сесії.

    Args:
        request: HTTP-запит.

    Returns:
        dict[str, int]: Словник кошика з ідентифікаторами аналізів.
    """
    return request.session.setdefault("cart", {})


def save_cart(request: HttpRequest, cart: dict[str, int]) -> None:
    """
    Зберігає кошик у сесії користувача.

    Args:
        request: HTTP-запит.
        cart: Словник кошика.

    Returns:
        None
    """
    request.session["cart"] = cart
    request.session.modified = True


def add_analysis_to_cart(request: HttpRequest, analysis_id: int) -> None:
    """
    Додає аналіз до кошика.

    Args:
        request: HTTP-запит.
        analysis_id: Ідентифікатор аналізу.

    Returns:
        None
    """
    cart = get_cart(request)
    cart[str(analysis_id)] = 1
    save_cart(request, cart)


def remove_analysis_from_cart(request: HttpRequest, analysis_id: int) -> None:
    """
    Видаляє аналіз із кошика.

    Args:
        request: HTTP-запит.
        analysis_id: Ідентифікатор аналізу.

    Returns:
        None
    """
    cart = get_cart(request)
    cart.pop(str(analysis_id), None)
    save_cart(request, cart)
