from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from accounts.constants import PATIENT_GROUP

User = get_user_model()


def patient_users_queryset() -> QuerySet[User]:
    """
    Повертає queryset користувачів із роллю пацієнта.

    Returns:
        QuerySet[User]: Набір користувачів, які належать до групи пацієнтів.
    """
    return User.objects.filter(groups__name=PATIENT_GROUP).distinct()


def is_patient(user: User) -> bool:
    """
    Перевіряє, чи належить користувач до групи пацієнтів.

    Args:
        user: Об'єкт користувача.

    Returns:
        bool: True, якщо користувач є пацієнтом.
    """
    return user.groups.filter(name=PATIENT_GROUP).exists()
