"""Модуль doctors/forms/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .direction import DirectionForm
from .doctor import DoctorForm
from .schedule import DoctorWorkDayForm, DoctorWorkPeriodForm, DoctorWorkPeriodFormSet
__all__ = ['DirectionForm', 'DoctorForm', 'DoctorWorkDayForm', 'DoctorWorkPeriodForm', 'DoctorWorkPeriodFormSet']
