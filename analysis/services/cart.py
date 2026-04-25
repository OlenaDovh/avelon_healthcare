"""Модуль `analysis/services/cart.py` застосунку `analysis`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.http import HttpRequest


def get_cart(request: HttpRequest) -> dict[str, int]:
    """Виконує прикладну логіку функції `get_cart` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        dict[str, int]: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return request.session.setdefault("cart", {})


def save_cart(request: HttpRequest, cart: dict[str, int]) -> None:
    """Виконує прикладну логіку функції `save_cart` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        cart: Значення типу `dict[str, int]`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    request.session["cart"] = cart
    request.session.modified = True


def add_analysis_to_cart(request: HttpRequest, analysis_id: int) -> None:
    """Виконує прикладну логіку функції `add_analysis_to_cart` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        analysis_id: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    cart = get_cart(request)
    cart[str(analysis_id)] = 1
    save_cart(request, cart)


def remove_analysis_from_cart(request: HttpRequest, analysis_id: int) -> None:
    """Виконує прикладну логіку функції `remove_analysis_from_cart` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        analysis_id: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    cart = get_cart(request)
    cart.pop(str(analysis_id), None)
    save_cart(request, cart)
