from __future__ import annotations

import pytest

from accounts.tokens import email_verification_token


@pytest.fixture
def verification_token(user) -> str:
    """
    Фікстура створює токен верифікації email для користувача.
    """
    return email_verification_token.make_token(user)


@pytest.mark.django_db
def test_email_verification_token_generated_for_user(verification_token: str) -> None:
    """
    Перевіряє, що токен генерується коректно.
    """
    assert verification_token
    assert isinstance(verification_token, str)


@pytest.mark.django_db
def test_email_verification_token_valid_for_same_user(user, verification_token: str) -> None:
    """
    Перевіряє валідність токена для того ж користувача.
    """
    assert email_verification_token.check_token(user, verification_token) is True


@pytest.mark.django_db
def test_token_invalid_for_other_user(user, user_factory, verification_token: str) -> None:
    """
    Перевіряє, що токен не валідний для іншого користувача.
    """
    other_user = user_factory()
    assert email_verification_token.check_token(other_user, verification_token) is False