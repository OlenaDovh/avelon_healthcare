"""Модуль avelon_healthcare/celery.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avelon_healthcare.settings.local')
app = Celery('avelon_healthcare')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
