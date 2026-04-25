"""Модуль accounts/selectors.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from accounts.constants import PATIENT_GROUP
User = get_user_model()

def patient_users_queryset() -> QuerySet[User]:
    """Виконує логіку `patient_users_queryset`.

Returns:
    Результат виконання операції."""
    return User.objects.filter(groups__name=PATIENT_GROUP).distinct()

def is_patient(user: User) -> bool:
    """Виконує логіку `is_patient`.

Args:
    user: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    return user.groups.filter(name=PATIENT_GROUP).exists()
