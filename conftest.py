"""Модуль `conftest.py` застосунку `conftest.py`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest
from django.contrib.auth import get_user_model
from pytest_factoryboy import register

from avelon_healthcare.tests.factories import (
    UserFactory,
    AnalysisFactory,
    ClinicInfoFactory,
    ContactInfoFactory,
    PromotionFactory,
    DirectionFactory,
    DoctorFactory,
    DoctorWorkDayFactory,
    DoctorWorkPeriodFactory,
    AppointmentFactory,
    OrderFactory,
    OrderItemFactory,
    ReviewFactory,
    SupportChatSessionFactory,
    SupportChatMessageFactory,
)

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
    """Виконує прикладну логіку функції `user` у відповідному модулі проєкту.

    Параметри:
        db: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return User.objects.create_user(
        email="user@example.com",
        password="testpass123",
        username="testuser",
        phone="+380991234567",
        first_name="Іван",
        last_name="Петренко",
    )


@pytest.fixture
def auth_client(client: Any, user: Any) -> Any:
    """Виконує прикладну логіку функції `auth_client` у відповідному модулі проєкту.

    Параметри:
        client: Значення типу `Any`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    client.force_login(user)
    return client
