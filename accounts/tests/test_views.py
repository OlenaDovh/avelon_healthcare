from typing import Any
import pytest
from django.urls import reverse
OPEN_PAGES = [('accounts:login', 'client'), ('accounts:register', 'client'), ('accounts:profile', 'auth_client'), ('accounts:profile_update', 'auth_client')]

def login_request(client: Any, login_value: str, password: str='testpass123') -> Any:
    """Виконує логіку `login_request`.

Args:
    client: Вхідний параметр `client`.
    login_value: Вхідний параметр `login_value`.
    password: Вхідний параметр `password`.

Returns:
    Any: Результат виконання."""
    return client.post(reverse('accounts:login'), {'username': login_value, 'password': password}, follow=True)

@pytest.mark.django_db
@pytest.mark.parametrize('url_name, client_fixture', OPEN_PAGES)
def test_page_opens(request: Any, url_name: Any, client_fixture: Any) -> None:
    """Виконує логіку `test_page_opens`.

Args:
    request: Вхідний параметр `request`.
    url_name: Вхідний параметр `url_name`.
    client_fixture: Вхідний параметр `client_fixture`.

Returns:
    Any: Результат виконання."""
    client = request.getfixturevalue(client_fixture)
    response = client.get(reverse(url_name))
    assert response.status_code == 200

@pytest.mark.django_db
def test_logout_redirects(auth_client: Any) -> None:
    """Виконує логіку `test_logout_redirects`.

Args:
    auth_client: Вхідний параметр `auth_client`.

Returns:
    Any: Результат виконання."""
    response = auth_client.get(reverse('accounts:logout'))
    assert response.status_code in (302, 301)

@pytest.mark.django_db
@pytest.mark.parametrize('login_attr', ['username', 'email'])
def test_user_can_login(client: Any, user: Any, login_attr: Any) -> None:
    """Виконує логіку `test_user_can_login`.

Args:
    client: Вхідний параметр `client`.
    user: Вхідний параметр `user`.
    login_attr: Вхідний параметр `login_attr`.

Returns:
    Any: Результат виконання."""
    response = login_request(client, getattr(user, login_attr))
    assert response.status_code == 200
