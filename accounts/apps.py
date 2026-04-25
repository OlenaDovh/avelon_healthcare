from __future__ import annotations

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Конфігурація застосунку accounts.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self) -> None:
        """
        Підключає сигнали застосунку.

        Returns:
            None
        """
        import accounts.signals