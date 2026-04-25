"""Модуль accounts/tests/test_tokens.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest
from accounts.tokens import email_verification_token

@pytest.fixture
def verification_token(user: Any) -> Any:
    """Виконує логіку `verification_token`.

Args:
    user: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    return email_verification_token.make_token(user)

@pytest.mark.django_db
def test_email_verification_token_generated_for_user(verification_token: Any) -> None:
    """Виконує логіку `test_email_verification_token_generated_for_user`.

Args:
    verification_token: Вхідне значення для виконання операції.

Returns:
    None."""
    assert verification_token
    assert isinstance(verification_token, str)

@pytest.mark.django_db
def test_email_verification_token_valid_for_same_user(user: Any, verification_token: Any) -> None:
    """Виконує логіку `test_email_verification_token_valid_for_same_user`.

Args:
    user: Вхідне значення для виконання операції.
    verification_token: Вхідне значення для виконання операції.

Returns:
    None."""
    assert email_verification_token.check_token(user, verification_token) is True

@pytest.mark.django_db
def test_token_invalid_for_other_user(user: Any, user_factory: Any, verification_token: Any) -> None:
    """Виконує логіку `test_token_invalid_for_other_user`.

Args:
    user: Вхідне значення для виконання операції.
    user_factory: Вхідне значення для виконання операції.
    verification_token: Вхідне значення для виконання операції.

Returns:
    None."""
    other_user = user_factory()
    assert email_verification_token.check_token(other_user, verification_token) is False
