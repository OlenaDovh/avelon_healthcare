"""Модуль doctors/apps.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.apps import AppConfig

class DoctorsConfig(AppConfig):
    """Клас DoctorsConfig.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctors'
