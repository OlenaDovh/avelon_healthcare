"""Модуль avelon_healthcare/settings/local.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .base import *
DEBUG = True
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = True
