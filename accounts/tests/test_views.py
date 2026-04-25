"""Модуль `accounts/tests/test_views.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest
from django.urls import reverse


OPEN_PAGES = [
    ("accounts:login", "client"),
    ("accounts:register", "client"),
    ("accounts:profile", "auth_client"),
    ("accounts:profile_update", "auth_client"),
]


def login_request(client: Any, login_value: str, password: str = "testpass123") -> Any:
    """Виконує прикладну логіку функції `login_request` у відповідному модулі проєкту.

    Параметри:
        client: Значення типу `Any`, яке передається для виконання логіки функції.
        login_value: Значення типу `str`, яке передається для виконання логіки функції.
        password: Значення типу `str`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
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
def test_page_opens(request: Any, url_name: Any, client_fixture: Any) -> None:
    """Виконує прикладну логіку функції `test_page_opens` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `Any`, яке передається для виконання логіки функції.
        url_name: Значення типу `Any`, яке передається для виконання логіки функції.
        client_fixture: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    client = request.getfixturevalue(client_fixture)
    response = client.get(reverse(url_name))
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_redirects(auth_client: Any) -> None:
    """Виконує прикладну логіку функції `test_logout_redirects` у відповідному модулі проєкту.

    Параметри:
        auth_client: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    response = auth_client.get(reverse("accounts:logout"))
    assert response.status_code in (302, 301)


@pytest.mark.django_db
@pytest.mark.parametrize("login_attr", ["username", "email"])
def test_user_can_login(client: Any, user: Any, login_attr: Any) -> None:
    """Виконує прикладну логіку функції `test_user_can_login` у відповідному модулі проєкту.

    Параметри:
        client: Значення типу `Any`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        login_attr: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    response = login_request(client, getattr(user, login_attr))
    assert response.status_code == 200
