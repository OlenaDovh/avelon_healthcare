"""Модуль `accounts/tests/test_signals.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest
from django.contrib.auth.models import Group

from accounts.constants import (
    PATIENT_GROUP,
    SUPPORT_GROUP,
    DOCTOR_GROUP,
)


def get_group(name: Any) -> Any:
    """Виконує прикладну логіку функції `get_group` у відповідному модулі проєкту.

    Параметри:
        name: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return Group.objects.get_or_create(name=name)[0]


@pytest.mark.django_db
def test_new_user_added_to_patient_group(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_new_user_added_to_patient_group` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user = user_factory()

    assert user.groups.filter(name=PATIENT_GROUP).exists()


@pytest.mark.django_db
@pytest.mark.parametrize("group_name", [SUPPORT_GROUP, DOCTOR_GROUP])
def test_user_becomes_staff_when_added_to_staff_groups(user_factory: Any, group_name: Any) -> None:
    """Виконує прикладну логіку функції `test_user_becomes_staff_when_added_to_staff_groups` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.
        group_name: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group = get_group(group_name)

    user = user_factory(is_staff=False)
    user.groups.add(group)
    user.refresh_from_db()

    assert user.is_staff is True
