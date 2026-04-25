"""Модуль appointments/forms/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .create import AppointmentCreateForm, GuestAppointmentCreateForm
from .support import SupportAppointmentCreateForm
from .update import SupportAppointmentUpdateForm
__all__ = ['AppointmentCreateForm', 'GuestAppointmentCreateForm', 'SupportAppointmentCreateForm', 'SupportAppointmentUpdateForm']
