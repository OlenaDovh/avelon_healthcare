"""Модуль avelon_healthcare/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .celery import app as celery_app
__all__ = ('celery_app',)
