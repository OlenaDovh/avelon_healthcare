from __future__ import annotations
from django.apps import AppConfig

class DoctorsConfig(AppConfig):
    """Описує клас `DoctorsConfig`."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctors'
