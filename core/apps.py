from __future__ import annotations
from django.apps import AppConfig

class CoreConfig(AppConfig):
    """Описує клас `CoreConfig`."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
