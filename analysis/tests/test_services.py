from __future__ import annotations

import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import RequestFactory

from analysis.services.cart import (
    add_analysis_to_cart,
    get_cart,
    remove_analysis_from_cart,
    save_cart,
)

pytestmark = pytest.mark.django_db


def add_session_to_request(request: HttpRequest) -> HttpRequest:
    """
    Додає session middleware до Django request для тестування.

    Args:
        request: Django HTTP request.

    Returns:
        HttpRequest: request із ініціалізованою session.
    """
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.fixture
def request_with_session() -> HttpRequest:
    """
    Фікстура, що повертає request із активною session.

    Returns:
        HttpRequest: request з session.
    """
    request = RequestFactory().get("/")
    return add_session_to_request(request)


def test_get_cart_returns_empty_cart_by_default(request_with_session: HttpRequest) -> None:
    """
    Перевіряє, що кошик за замовчуванням порожній.
    """
    cart = get_cart(request_with_session)

    assert cart == {}
    assert request_with_session.session["cart"] == {}


def test_save_cart_updates_session(request_with_session: HttpRequest) -> None:
    """
    Перевіряє, що save_cart оновлює session.
    """
    cart: dict[str, int] = {"1": 1}

    save_cart(request_with_session, cart)

    assert request_with_session.session["cart"] == {"1": 1}
    assert request_with_session.session.modified is True


def test_add_analysis_to_cart(request_with_session: HttpRequest) -> None:
    """
    Перевіряє додавання аналізу до кошика.
    """
    add_analysis_to_cart(request_with_session, 5)

    assert request_with_session.session["cart"] == {"5": 1}


def test_remove_analysis_from_cart(request_with_session: HttpRequest) -> None:
    """
    Перевіряє видалення аналізу з кошика.
    """
    request_with_session.session["cart"] = {"5": 1, "8": 1}
    request_with_session.session.save()

    remove_analysis_from_cart(request_with_session, 5)

    assert request_with_session.session["cart"] == {"8": 1}