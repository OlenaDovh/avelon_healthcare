from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from accounts.constants import PATIENT_GROUP

User = get_user_model()


def patient_users_queryset() -> QuerySet[User]:
    return User.objects.filter(groups__name=PATIENT_GROUP).distinct()


def is_patient(user: User) -> bool:
    return user.groups.filter(name=PATIENT_GROUP).exists()