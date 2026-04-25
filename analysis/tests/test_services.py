"""Модуль `analysis/tests/test_services.py` застосунку `analysis`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from analysis.services.cart import (
    add_analysis_to_cart,
    get_cart,
    remove_analysis_from_cart,
    save_cart,
)

pytestmark = pytest.mark.django_db


def add_session_to_request(request: Any) -> Any:
    """Виконує прикладну логіку функції `add_session_to_request` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.fixture
def request_with_session() -> Any:
    """Виконує прикладну логіку функції `request_with_session` у відповідному модулі проєкту.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    request = RequestFactory().get("/")
    return add_session_to_request(request)


def test_get_cart_returns_empty_cart_by_default(request_with_session: Any) -> None:
    """Виконує прикладну логіку функції `test_get_cart_returns_empty_cart_by_default` у відповідному модулі проєкту.

    Параметри:
        request_with_session: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    cart = get_cart(request_with_session)

    assert cart == {}
    assert request_with_session.session["cart"] == {}


def test_save_cart_updates_session(request_with_session: Any) -> None:
    """Виконує прикладну логіку функції `test_save_cart_updates_session` у відповідному модулі проєкту.

    Параметри:
        request_with_session: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    cart = {"1": 1}

    save_cart(request_with_session, cart)

    assert request_with_session.session["cart"] == {"1": 1}
    assert request_with_session.session.modified is True


def test_add_analysis_to_cart(request_with_session: Any) -> None:
    """Виконує прикладну логіку функції `test_add_analysis_to_cart` у відповідному модулі проєкту.

    Параметри:
        request_with_session: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    add_analysis_to_cart(request_with_session, 5)

    assert request_with_session.session["cart"] == {"5": 1}


def test_remove_analysis_from_cart(request_with_session: Any) -> None:
    """Виконує прикладну логіку функції `test_remove_analysis_from_cart` у відповідному модулі проєкту.

    Параметри:
        request_with_session: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    request_with_session.session["cart"] = {"5": 1, "8": 1}
    request_with_session.session.save()

    remove_analysis_from_cart(request_with_session, 5)

    assert request_with_session.session["cart"] == {"8": 1}
