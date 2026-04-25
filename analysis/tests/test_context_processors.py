from __future__ import annotations

from django.http import HttpRequest

from analysis.context_processors import cart_items_count


def test_cart_items_count_returns_zero_for_empty_session(rf) -> None:
    """
    Перевіряє, що для порожньої сесії повертається 0 елементів кошика.
    """
    request: HttpRequest = rf.get("/")
    request.session = {}

    result = cart_items_count(request)

    assert result == {"cart_items_count": 0}


def test_cart_items_count_returns_cart_length(rf) -> None:
    """
    Перевіряє, що повертається кількість елементів у кошику.
    """
    request: HttpRequest = rf.get("/")
    request.session = {"cart": {"1": 1, "2": 1, "3": 1}}

    result = cart_items_count(request)

    assert result == {"cart_items_count": 3}