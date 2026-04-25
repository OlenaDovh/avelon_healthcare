"""Модуль `accounts/tests/test_selectors.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest

from accounts.selectors import patient_users_queryset, is_patient


@pytest.mark.django_db
def test_patient_users_queryset_returns_all_created_users(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_patient_users_queryset_returns_all_created_users` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user1 = user_factory()
    user2 = user_factory()

    result = patient_users_queryset()

    assert user1 in result
    assert user2 in result


@pytest.mark.django_db
def test_is_patient_returns_true_for_created_user(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_is_patient_returns_true_for_created_user` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user = user_factory()

    assert is_patient(user) is True
