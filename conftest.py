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
def user(db):
    """
    Виконує логіку `user`.

    Args:
        db: Вхідний параметр `db`.

    Returns:
        Any: Результат виконання.
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
def auth_client(client, user):
    """
    Виконує логіку `auth_client`.

    Args:
        client: Вхідний параметр `client`.
        user: Вхідний параметр `user`.

    Returns:
        Any: Результат виконання.
     """
    client.force_login(user)
    return client
