"""Модуль accounts/forms/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .auth import LoginForm, RegisterForm
from .passwords import UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from .profile import ProfileUpdateForm
from .support import SupportPatientUpdateForm
