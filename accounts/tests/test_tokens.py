"""Модуль `accounts/tests/test_tokens.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest

from accounts.tokens import email_verification_token


@pytest.fixture
def verification_token(user: Any) -> Any:
    """Виконує прикладну логіку функції `verification_token` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return email_verification_token.make_token(user)

@pytest.mark.django_db
def test_email_verification_token_generated_for_user(verification_token: Any) -> None:
    """Виконує прикладну логіку функції `test_email_verification_token_generated_for_user` у відповідному модулі проєкту.

    Параметри:
        verification_token: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    assert verification_token
    assert isinstance(verification_token, str)

@pytest.mark.django_db
def test_email_verification_token_valid_for_same_user(user: Any, verification_token: Any) -> None:
    """Виконує прикладну логіку функції `test_email_verification_token_valid_for_same_user` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        verification_token: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    assert email_verification_token.check_token(user, verification_token) is True

@pytest.mark.django_db
def test_token_invalid_for_other_user(user: Any, user_factory: Any, verification_token: Any) -> None:
    """Виконує прикладну логіку функції `test_token_invalid_for_other_user` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.
        verification_token: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    other_user = user_factory()
    assert email_verification_token.check_token(other_user, verification_token) is False
