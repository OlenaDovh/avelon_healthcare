"""Модуль conftest.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest
from django.contrib.auth import get_user_model
from pytest_factoryboy import register
from avelon_healthcare.tests.factories import UserFactory, AnalysisFactory, ClinicInfoFactory, ContactInfoFactory, PromotionFactory, DirectionFactory, DoctorFactory, DoctorWorkDayFactory, DoctorWorkPeriodFactory, AppointmentFactory, OrderFactory, OrderItemFactory, ReviewFactory, SupportChatSessionFactory, SupportChatMessageFactory
User = get_user_model()
register(UserFactory)
register(AnalysisFactory)
register(ClinicInfoFactory)
register(ContactInfoFactory)
register(PromotionFactory)
register(DirectionFactory)
register(DoctorFactory)
register(DoctorWorkDayFactory)
register(DoctorWorkPeriodFactory)
register(AppointmentFactory)
register(OrderFactory)
register(OrderItemFactory)
register(ReviewFactory)
register(SupportChatSessionFactory)
register(SupportChatMessageFactory)

@pytest.fixture
def user(db: Any) -> Any:
    """Виконує логіку `user`.

Args:
    db: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    return User.objects.create_user(email='user@example.com', password='testpass123', username='testuser', phone='+380991234567', first_name='Іван', last_name='Петренко')

@pytest.fixture
def auth_client(client: Any, user: Any) -> Any:
    """Виконує логіку `auth_client`.

Args:
    client: Вхідне значення для виконання операції.
    user: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    client.force_login(user)
    return client
