"""Модуль `accounts/selectors.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from accounts.constants import PATIENT_GROUP

User = get_user_model()


def patient_users_queryset() -> QuerySet[User]:
    """Виконує прикладну логіку функції `patient_users_queryset` у відповідному модулі проєкту.

    Повертає:
        QuerySet[User]: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return User.objects.filter(groups__name=PATIENT_GROUP).distinct()


def is_patient(user: User) -> bool:
    """Виконує прикладну логіку функції `is_patient` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `User`, яке передається для виконання логіки функції.

    Повертає:
        bool: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    return user.groups.filter(name=PATIENT_GROUP).exists()
