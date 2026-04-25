from typing import Any
import pytest
from accounts.tokens import email_verification_token

@pytest.fixture
def verification_token(user: Any) -> Any:
    """Виконує логіку `verification_token`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    return email_verification_token.make_token(user)

@pytest.mark.django_db
def test_email_verification_token_generated_for_user(verification_token: Any) -> None:
    """Виконує логіку `test_email_verification_token_generated_for_user`.

Args:
    verification_token: Вхідний параметр `verification_token`.

Returns:
    Any: Результат виконання."""
    assert verification_token
    assert isinstance(verification_token, str)

@pytest.mark.django_db
def test_email_verification_token_valid_for_same_user(user: Any, verification_token: Any) -> None:
    """Виконує логіку `test_email_verification_token_valid_for_same_user`.

Args:
    user: Вхідний параметр `user`.
    verification_token: Вхідний параметр `verification_token`.

Returns:
    Any: Результат виконання."""
    assert email_verification_token.check_token(user, verification_token) is True

@pytest.mark.django_db
def test_token_invalid_for_other_user(user: Any, user_factory: Any, verification_token: Any) -> None:
    """Виконує логіку `test_token_invalid_for_other_user`.

Args:
    user: Вхідний параметр `user`.
    user_factory: Вхідний параметр `user_factory`.
    verification_token: Вхідний параметр `verification_token`.

Returns:
    Any: Результат виконання."""
    other_user = user_factory()
    assert email_verification_token.check_token(other_user, verification_token) is False
