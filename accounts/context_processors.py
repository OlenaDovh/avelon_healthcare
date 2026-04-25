from __future__ import annotations
from django.http import HttpRequest
from accounts.constants import CONTENT_MANAGER_GROUP, DOCTOR_GROUP, HEAD_MANAGER_GROUP, PATIENT_GROUP, SUPPORT_GROUP

def user_roles(request: HttpRequest) -> dict[str, bool]:
    """Виконує логіку `user_roles`.

Args:
    request: Вхідний параметр `request`.

Returns:
    Any: Результат виконання."""
    user = request.user
    if not user.is_authenticated:
        return {'is_patient': False, 'is_support': False, 'is_doctor': False, 'is_head_manager': False, 'is_content_manager': False, 'is_staff_role': False, 'is_superadmin': False}
    group_names = set(user.groups.values_list('name', flat=True))
    is_support = SUPPORT_GROUP in group_names
    is_doctor = DOCTOR_GROUP in group_names
    is_head_manager = HEAD_MANAGER_GROUP in group_names
    is_content_manager = CONTENT_MANAGER_GROUP in group_names
    is_superadmin = user.is_superuser
    is_staff_role = any((is_support, is_doctor, is_head_manager, is_content_manager, is_superadmin))
    return {'is_patient': PATIENT_GROUP in group_names, 'is_support': is_support, 'is_doctor': is_doctor, 'is_head_manager': is_head_manager, 'is_content_manager': is_content_manager, 'is_staff_role': is_staff_role, 'is_superadmin': is_superadmin}
