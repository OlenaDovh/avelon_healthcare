from __future__ import annotations
import pytest
from django.contrib.auth.models import Group

from accounts.constants import (
    CONTENT_MANAGER_GROUP,
    DOCTOR_GROUP,
    HEAD_MANAGER_GROUP,
    PATIENT_GROUP,
    SUPPORT_GROUP,
)
from accounts.permissions import (
    has_group,
    is_content_manager,
    is_doctor,
    is_head_manager,
    is_patient,
    is_staff_role,
    is_support,
)


def create_user_with_group(user_factory, group_name: str):
    """
    Створює користувача та додає його до вказаної групи.

    Args:
        user_factory: Фабрика користувачів.
        group_name: Назва групи.

    Returns:
        Користувач із доданою групою.
    """
    group, _ = Group.objects.get_or_create(name=group_name)
    user = user_factory()
    user.groups.add(group)
    return user


@pytest.mark.django_db
def test_has_group_returns_true(user_factory) -> None:
    """
    Перевіряє, що has_group повертає True для користувача з групою.
    """
    user = create_user_with_group(user_factory, PATIENT_GROUP)

    assert has_group(user, PATIENT_GROUP) is True


@pytest.mark.django_db
def test_has_group_returns_true_for_default_patient(user_factory) -> None:
    """
    Перевіряє, що користувач за замовчуванням належить до групи PATIENT.
    """
    user = user_factory()

    assert has_group(user, PATIENT_GROUP) is True


def test_has_group_returns_false_for_anonymous() -> None:
    """
    Перевіряє, що has_group повертає False для анонімного користувача.
    """
    class AnonymousUser:
        is_authenticated = False

    assert has_group(AnonymousUser(), PATIENT_GROUP) is False


@pytest.mark.django_db
def test_is_patient(user_factory) -> None:
    """
    Перевіряє функцію is_patient.
    """
    user = create_user_with_group(user_factory, PATIENT_GROUP)

    assert is_patient(user) is True


@pytest.mark.django_db
def test_is_support(user_factory) -> None:
    """
    Перевіряє функцію is_support.
    """
    user = create_user_with_group(user_factory, SUPPORT_GROUP)

    assert is_support(user) is True


@pytest.mark.django_db
def test_is_doctor(user_factory) -> None:
    """
    Перевіряє функцію is_doctor.
    """
    user = create_user_with_group(user_factory, DOCTOR_GROUP)

    assert is_doctor(user) is True


@pytest.mark.django_db
def test_is_head_manager(user_factory) -> None:
    """
    Перевіряє функцію is_head_manager.
    """
    user = create_user_with_group(user_factory, HEAD_MANAGER_GROUP)

    assert is_head_manager(user) is True


@pytest.mark.django_db
def test_is_content_manager(user_factory) -> None:
    """
    Перевіряє функцію is_content_manager.
    """
    user = create_user_with_group(user_factory, CONTENT_MANAGER_GROUP)

    assert is_content_manager(user) is True


@pytest.mark.django_db
def test_is_staff_role_returns_true_for_staff_group(user_factory) -> None:
    """
    Перевіряє, що is_staff_role повертає True для staff-групи.
    """
    user = create_user_with_group(user_factory, SUPPORT_GROUP)

    assert is_staff_role(user) is True


@pytest.mark.django_db
def test_is_staff_role_returns_true_for_superuser(user_factory) -> None:
    """
    Перевіряє, що is_staff_role повертає True для суперкористувача.
    """
    user = user_factory(is_superuser=True)

    assert is_staff_role(user) is True


@pytest.mark.django_db
def test_is_staff_role_returns_false_for_regular_user(user_factory) -> None:
    """
    Перевіряє, що is_staff_role повертає False для звичайного користувача.
    """
    user = user_factory()
    user.groups.clear()

    assert is_staff_role(user) is False