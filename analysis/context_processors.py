"""Модуль `analysis/context_processors.py` застосунку `analysis`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.http import HttpRequest


def cart_items_count(request: HttpRequest) -> dict[str, int]:
    """
    Додає кількість елементів кошика в контекст шаблонів.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        dict[str, int]: Кількість елементів кошика.
    """
    cart: dict[str, int] = request.session.get("cart", {})
    return {
        "cart_items_count": len(cart),
    }
