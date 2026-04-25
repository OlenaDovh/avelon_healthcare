"""Модуль accounts/views/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .auth import login_view, logout_view, register_view, resend_verification_email_view, verify_email_view
from .passwords import UserPasswordResetView, password_change_view
from .profile import profile_update_view, profile_view, staff_dashboard_view
from .support import support_patient_list_view, support_patient_update_view
