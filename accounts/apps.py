"""Модуль accounts/apps.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    """Клас AccountsConfig.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self) -> None:
        """Виконує логіку `ready`.

Returns:
    None."""
        import accounts.signals
