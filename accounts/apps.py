"""Модуль `accounts/apps.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

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
