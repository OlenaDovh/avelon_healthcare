"""Модуль analysis/tests/test_views.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from accounts.constants import HEAD_MANAGER_GROUP

def create_head_manager(user: Any) -> Any:
    """Виконує логіку `create_head_manager`.

Args:
    user: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    group, _ = Group.objects.get_or_create(name=HEAD_MANAGER_GROUP)
    user.groups.add(group)
    return user

@pytest.mark.django_db
def test_analysis_list_view_opens(client: Any, analysis_factory: Any) -> None:
    """Виконує логіку `test_analysis_list_view_opens`.

Args:
    client: Вхідне значення для виконання операції.
    analysis_factory: Вхідне значення для виконання операції.

Returns:
    None."""
    analysis_factory(is_active=True)
    response = client.get(reverse('analysis:analysis_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_to_cart_view_redirects_and_adds_item(client: Any, analysis: Any) -> None:
    """Виконує логіку `test_add_to_cart_view_redirects_and_adds_item`.

Args:
    client: Вхідне значення для виконання операції.
    analysis: Вхідне значення для виконання операції.

Returns:
    None."""
    session = client.session
    session['cart'] = {}
    session.save()
    response = client.get(reverse('analysis:add_to_cart', args=[analysis.id]))
    assert response.status_code in (302, 301)
    session = client.session
    assert str(analysis.id) in session['cart']

@pytest.mark.django_db
def test_remove_from_cart_view_redirects_and_removes_item(client: Any, analysis: Any) -> None:
    """Виконує логіку `test_remove_from_cart_view_redirects_and_removes_item`.

Args:
    client: Вхідне значення для виконання операції.
    analysis: Вхідне значення для виконання операції.

Returns:
    None."""
    session = client.session
    session['cart'] = {str(analysis.id): 1}
    session.save()
    response = client.get(reverse('analysis:remove_from_cart', args=[analysis.id]))
    assert response.status_code in (302, 301)
    session = client.session
    assert str(analysis.id) not in session['cart']

@pytest.mark.django_db
def test_cart_detail_view_opens(client: Any, analysis: Any) -> None:
    """Виконує логіку `test_cart_detail_view_opens`.

Args:
    client: Вхідне значення для виконання операції.
    analysis: Вхідне значення для виконання операції.

Returns:
    None."""
    session = client.session
    session['cart'] = {str(analysis.id): 1}
    session.save()
    response = client.get(reverse('analysis:cart_detail'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_head_manager_analysis_list_view_opens_for_head_manager(client: Any, user: Any, analysis_factory: Any) -> None:
    """Виконує логіку `test_head_manager_analysis_list_view_opens_for_head_manager`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.
    analysis_factory: Вхідне значення для виконання операції.

Returns:
    None."""
    create_head_manager(user)
    client.force_login(user)
    analysis_factory()
    response = client.get(reverse('analysis:head_manager_analysis_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_head_manager_analysis_create_view_get_opens_for_head_manager(client: Any, user: Any) -> None:
    """Виконує логіку `test_head_manager_analysis_create_view_get_opens_for_head_manager`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.

Returns:
    None."""
    create_head_manager(user)
    client.force_login(user)
    response = client.get(reverse('analysis:head_manager_analysis_create'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_head_manager_analysis_create_view_post_creates_analysis(client: Any, user: Any) -> None:
    """Виконує логіку `test_head_manager_analysis_create_view_post_creates_analysis`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.

Returns:
    None."""
    create_head_manager(user)
    client.force_login(user)
    response = client.post(reverse('analysis:head_manager_analysis_create'), {'name': 'Новий аналіз', 'what_to_check': 'Гемоглобін', 'disease': 'Анемія', 'for_whom': 'Для дорослих', 'biomaterial': 'Кров', 'duration_days': 2, 'price': '500.00', 'is_active': True}, follow=True)
    assert response.status_code == 200

@pytest.mark.django_db
def test_head_manager_analysis_update_view_get_opens_for_head_manager(client: Any, user: Any, analysis: Any) -> None:
    """Виконує логіку `test_head_manager_analysis_update_view_get_opens_for_head_manager`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.
    analysis: Вхідне значення для виконання операції.

Returns:
    None."""
    create_head_manager(user)
    client.force_login(user)
    response = client.get(reverse('analysis:head_manager_analysis_update', args=[analysis.pk]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_head_manager_analysis_update_view_post_updates_analysis(client: Any, user: Any, analysis: Any) -> None:
    """Виконує логіку `test_head_manager_analysis_update_view_post_updates_analysis`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.
    analysis: Вхідне значення для виконання операції.

Returns:
    None."""
    create_head_manager(user)
    client.force_login(user)
    response = client.post(reverse('analysis:head_manager_analysis_update', args=[analysis.pk]), {'name': 'Оновлений аналіз', 'what_to_check': analysis.what_to_check, 'disease': analysis.disease, 'for_whom': analysis.for_whom, 'biomaterial': analysis.biomaterial, 'duration_days': analysis.duration_days, 'price': analysis.price, 'is_active': analysis.is_active}, follow=True)
    assert response.status_code == 200
    analysis.refresh_from_db()
    assert analysis.name == 'Оновлений аналіз'
