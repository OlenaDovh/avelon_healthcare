"""Модуль accounts/tests/test_models.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest

@pytest.mark.django_db
def test_user_factory_creates_user(user: Any) -> None:
    """Виконує логіку `test_user_factory_creates_user`.

Args:
    user: Вхідне значення для виконання операції.

Returns:
    None."""
    assert user.id is not None
    assert user.email
    assert user.phone
    assert user.username

@pytest.mark.django_db
def test_user_full_name_property(user: Any) -> None:
    """Виконує логіку `test_user_full_name_property`.

Args:
    user: Вхідне значення для виконання операції.

Returns:
    None."""
    expected = ' '.join(filter(None, [user.last_name, user.first_name, user.middle_name]))
    assert user.full_name == expected

@pytest.mark.django_db
def test_user_str_returns_full_name(user: Any) -> None:
    """Виконує логіку `test_user_str_returns_full_name`.

Args:
    user: Вхідне значення для виконання операції.

Returns:
    None."""
    assert str(user) == user.full_name
