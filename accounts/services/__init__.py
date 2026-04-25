"""Модуль accounts/services/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .email_verification import build_email_verification_url, send_verification_email
from .roles import assign_group_permissions, setup_roles
