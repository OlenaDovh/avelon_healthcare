"""Модуль `accounts/tests/test_models.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest


@pytest.mark.django_db
def test_user_factory_creates_user(user: Any) -> None:
    """Виконує прикладну логіку функції `test_user_factory_creates_user` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    assert user.id is not None
    assert user.email
    assert user.phone
    assert user.username


@pytest.mark.django_db
def test_user_full_name_property(user: Any) -> None:
    """Виконує прикладну логіку функції `test_user_full_name_property` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    expected = " ".join(filter(None, [user.last_name, user.first_name, user.middle_name]))
    assert user.full_name == expected


@pytest.mark.django_db
def test_user_str_returns_full_name(user: Any) -> None:
    """Виконує прикладну логіку функції `test_user_str_returns_full_name` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    assert str(user) == user.full_name
