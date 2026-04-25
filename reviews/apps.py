"""Модуль reviews/apps.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    """Клас ReviewsConfig.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    name = 'reviews'
