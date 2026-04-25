from __future__ import annotations
import pytest
from accounts.selectors import patient_users_queryset, is_patient


@pytest.mark.django_db
def test_patient_users_queryset_returns_all_created_users(user_factory) -> None:
    """
    Перевіряє, що patient_users_queryset повертає всіх створених користувачів.
    """
    user1 = user_factory()
    user2 = user_factory()

    result = patient_users_queryset()

    assert user1 in result
    assert user2 in result


@pytest.mark.django_db
def test_is_patient_returns_true_for_created_user(user_factory) -> None:
    """
    Перевіряє, що is_patient повертає True для створеного користувача.
    """
    user = user_factory()

    assert is_patient(user) is True
