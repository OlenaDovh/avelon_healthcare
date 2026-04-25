"""Модуль accounts/permissions/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .decorators import content_manager_required, doctor_required, head_manager_required, support_required
from .predicates import has_group, is_content_manager, is_doctor, is_head_manager, is_patient, is_staff_role, is_support
__all__ = ['has_group', 'is_patient', 'is_support', 'is_doctor', 'is_head_manager', 'is_content_manager', 'is_staff_role', 'support_required', 'doctor_required', 'head_manager_required', 'content_manager_required']
