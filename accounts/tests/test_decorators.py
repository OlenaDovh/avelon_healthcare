"""Модуль `accounts/tests/test_decorators.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory

from accounts.constants import SUPPORT_GROUP
from accounts.permissions import support_required, is_support
from accounts.permissions.decorators import role_required


def dummy_view(request: Any) -> Any:
    """Виконує прикладну логіку функції `dummy_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return HttpResponse("OK")


@pytest.mark.django_db
def test_role_required_allows_user_with_role(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_role_required_allows_user_with_role` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group, _ = Group.objects.get_or_create(name=SUPPORT_GROUP)
    user = user_factory()
    user.groups.add(group)

    request = RequestFactory().get("/")
    request.user = user

    protected_view = role_required(is_support)(dummy_view)
    response = protected_view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_role_required_allows_superuser(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_role_required_allows_superuser` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user = user_factory(is_superuser=True)

    request = RequestFactory().get("/")
    request.user = user

    protected_view = role_required(is_support)(dummy_view)
    response = protected_view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_role_required_raises_permission_denied_for_user_without_role(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_role_required_raises_permission_denied_for_user_without_role` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    user = user_factory()

    request = RequestFactory().get("/")
    request.user = user

    protected_view = role_required(is_support)(dummy_view)

    with pytest.raises(PermissionDenied):
        protected_view(request)


@pytest.mark.django_db
def test_support_required_allows_support_user(user_factory: Any) -> None:
    """Виконує прикладну логіку функції `test_support_required_allows_support_user` у відповідному модулі проєкту.

    Параметри:
        user_factory: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    group, _ = Group.objects.get_or_create(name=SUPPORT_GROUP)
    user = user_factory()
    user.groups.add(group)

    request = RequestFactory().get("/")
    request.user = user

    response = support_required(dummy_view)(request)

    assert response.status_code == 200
