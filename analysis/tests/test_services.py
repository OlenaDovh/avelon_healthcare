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


def add_session_to_request(request):
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.fixture
def request_with_session():
    request = RequestFactory().get("/")
    return add_session_to_request(request)


def test_get_cart_returns_empty_cart_by_default(request_with_session):
    cart = get_cart(request_with_session)

    assert cart == {}
    assert request_with_session.session["cart"] == {}


def test_save_cart_updates_session(request_with_session):
    cart = {"1": 1}

    save_cart(request_with_session, cart)

    assert request_with_session.session["cart"] == {"1": 1}
    assert request_with_session.session.modified is True


def test_add_analysis_to_cart(request_with_session):
    add_analysis_to_cart(request_with_session, 5)

    assert request_with_session.session["cart"] == {"5": 1}


def test_remove_analysis_from_cart(request_with_session):
    request_with_session.session["cart"] = {"5": 1, "8": 1}
    request_with_session.session.save()

    remove_analysis_from_cart(request_with_session, 5)

    assert request_with_session.session["cart"] == {"8": 1}