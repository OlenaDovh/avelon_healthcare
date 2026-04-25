from __future__ import annotations

import pytest
from django.urls import reverse


OPEN_PAGES: list[tuple[str, str]] = [
    ("accounts:login", "client"),
    ("accounts:register", "client"),
    ("accounts:profile", "auth_client"),
    ("accounts:profile_update", "auth_client"),
]


def login_request(client, login_value: str, password: str = "testpass123"):
    """
    Виконує POST-запит на логін користувача.

    Args:
        client: Django test client.
        login_value: username або email.
        password: пароль користувача.

    Returns:
        Response: результат запиту.
    """
    return client.post(
        reverse("accounts:login"),
        {
            "username": login_value,
            "password": password,
        },
        follow=True,
    )


@pytest.mark.django_db
@pytest.mark.parametrize("url_name, client_fixture", OPEN_PAGES)
def test_page_opens(request, url_name: str, client_fixture: str) -> None:
    """
    Перевіряє, що сторінки відкриваються без помилок.
    """
    client = request.getfixturevalue(client_fixture)
    response = client.get(reverse(url_name))
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_redirects(auth_client) -> None:
    """
    Перевіряє редірект після logout.
    """
    response = auth_client.get(reverse("accounts:logout"))
    assert response.status_code in (302, 301)


@pytest.mark.django_db
@pytest.mark.parametrize("login_attr", ["username", "email"])
def test_user_can_login(client, user, login_attr: str) -> None:
    """
    Перевіряє можливість логіну через username або email.
    """
    response = login_request(client, getattr(user, login_attr))
    assert response.status_code == 200