from typing import Any
import pytest

@pytest.mark.django_db
def test_user_factory_creates_user(user: Any) -> None:
    """Виконує логіку `test_user_factory_creates_user`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    assert user.id is not None
    assert user.email
    assert user.phone
    assert user.username

@pytest.mark.django_db
def test_user_full_name_property(user: Any) -> None:
    """Виконує логіку `test_user_full_name_property`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    expected = ' '.join(filter(None, [user.last_name, user.first_name, user.middle_name]))
    assert user.full_name == expected

@pytest.mark.django_db
def test_user_str_returns_full_name(user: Any) -> None:
    """Виконує логіку `test_user_str_returns_full_name`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    assert str(user) == user.full_name
