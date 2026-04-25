"""Модуль appointments/views/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .ajax import available_dates, available_doctors, available_slots
from .patient import appointment_cancel_view, appointment_detail_view, appointment_list_view
from .public import appointment_create_view
from .support import support_appointment_create_view, support_appointment_list_view, support_appointment_update_view
