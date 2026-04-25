"""Модуль accounts/tests/test_decorators.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
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
    """Виконує логіку `dummy_view`.

Args:
    request: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    return HttpResponse('OK')

@pytest.mark.django_db
def test_role_required_allows_user_with_role(user_factory: Any) -> None:
    """Виконує логіку `test_role_required_allows_user_with_role`.

Args:
    user_factory: Вхідне значення для виконання операції.

Returns:
    None."""
    group, _ = Group.objects.get_or_create(name=SUPPORT_GROUP)
    user = user_factory()
    user.groups.add(group)
    request = RequestFactory().get('/')
    request.user = user
    protected_view = role_required(is_support)(dummy_view)
    response = protected_view(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_role_required_allows_superuser(user_factory: Any) -> None:
    """Виконує логіку `test_role_required_allows_superuser`.

Args:
    user_factory: Вхідне значення для виконання операції.

Returns:
    None."""
    user = user_factory(is_superuser=True)
    request = RequestFactory().get('/')
    request.user = user
    protected_view = role_required(is_support)(dummy_view)
    response = protected_view(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_role_required_raises_permission_denied_for_user_without_role(user_factory: Any) -> None:
    """Виконує логіку `test_role_required_raises_permission_denied_for_user_without_role`.

Args:
    user_factory: Вхідне значення для виконання операції.

Returns:
    None."""
    user = user_factory()
    request = RequestFactory().get('/')
    request.user = user
    protected_view = role_required(is_support)(dummy_view)
    with pytest.raises(PermissionDenied):
        protected_view(request)

@pytest.mark.django_db
def test_support_required_allows_support_user(user_factory: Any) -> None:
    """Виконує логіку `test_support_required_allows_support_user`.

Args:
    user_factory: Вхідне значення для виконання операції.

Returns:
    None."""
    group, _ = Group.objects.get_or_create(name=SUPPORT_GROUP)
    user = user_factory()
    user.groups.add(group)
    request = RequestFactory().get('/')
    request.user = user
    response = support_required(dummy_view)(request)
    assert response.status_code == 200
