"""Модуль `accounts/tests/test_predicates.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
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


@pytest.mark.django_db
def test_has_group_returns_true(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_has_group_returns_true` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group, _ = Group.objects.get_or_create(name=PATIENT_GROUP)
    user = user_factory()
    user.groups.add(group)

    assert has_group(user, PATIENT_GROUP) is True


@pytest.mark.django_db
def test_has_group_returns_true_for_default_patient(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_has_group_returns_true_for_default_patient` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user = user_factory()

    assert has_group(user, PATIENT_GROUP) is True


def test_has_group_returns_false_for_anonymous() -> None:
    """Виконує прикладну логіку функції `test_has_group_returns_false_for_anonymous` у відповідному модулі проєкту.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    class AnonymousUser:
        """Клас `AnonymousUser` інкапсулює повʼязану логіку проєкту.

        Базові класи: `object`.
        Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
        """
        is_authenticated = False

    assert has_group(AnonymousUser(), PATIENT_GROUP) is False


@pytest.mark.django_db
def test_is_patient(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_is_patient` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group, _ = Group.objects.get_or_create(name=PATIENT_GROUP)
    user = user_factory()
    user.groups.add(group)

    assert is_patient(user) is True


@pytest.mark.django_db
def test_is_support(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_is_support` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group, _ = Group.objects.get_or_create(name=SUPPORT_GROUP)
    user = user_factory()
    user.groups.add(group)

    assert is_support(user) is True


@pytest.mark.django_db
def test_is_doctor(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_is_doctor` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group, _ = Group.objects.get_or_create(name=DOCTOR_GROUP)
    user = user_factory()
    user.groups.add(group)

    assert is_doctor(user) is True


@pytest.mark.django_db
def test_is_head_manager(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_is_head_manager` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group, _ = Group.objects.get_or_create(name=HEAD_MANAGER_GROUP)
    user = user_factory()
    user.groups.add(group)

    assert is_head_manager(user) is True


@pytest.mark.django_db
def test_is_content_manager(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_is_content_manager` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group, _ = Group.objects.get_or_create(name=CONTENT_MANAGER_GROUP)
    user = user_factory()
    user.groups.add(group)

    assert is_content_manager(user) is True


@pytest.mark.django_db
def test_is_staff_role_returns_true_for_staff_group(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_is_staff_role_returns_true_for_staff_group` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group, _ = Group.objects.get_or_create(name=SUPPORT_GROUP)
    user = user_factory()
    user.groups.add(group)

    assert is_staff_role(user) is True


@pytest.mark.django_db
def test_is_staff_role_returns_true_for_superuser(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_is_staff_role_returns_true_for_superuser` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user = user_factory(is_superuser=True)

    assert is_staff_role(user) is True


@pytest.mark.django_db
def test_is_staff_role_returns_false_for_regular_user(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_is_staff_role_returns_false_for_regular_user` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user = user_factory()

    assert is_staff_role(user) is False
