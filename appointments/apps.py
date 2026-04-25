"""Модуль appointments/apps.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.apps import AppConfig

class AppointmentsConfig(AppConfig):
    """Клас AppointmentsConfig.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    name = 'appointments'
