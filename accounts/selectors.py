from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()

PATIENT_GROUP_NAME: str = "patient"


def patient_users_queryset() -> QuerySet[User]:
    return User.objects.filter(groups__name=PATIENT_GROUP_NAME).distinct()


def is_patient(user: User) -> bool:
    return user.groups.filter(name=PATIENT_GROUP_NAME).exists()