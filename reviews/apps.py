from __future__ import annotations
from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Конфігурація застосунку reviews.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "reviews"
