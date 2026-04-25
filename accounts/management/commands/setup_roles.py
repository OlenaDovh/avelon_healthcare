"""Модуль accounts/management/commands/setup_roles.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.core.management.base import BaseCommand
from accounts.services import assign_group_permissions

class Command(BaseCommand):
    """Клас Command.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    help = 'Create groups and assign permissions'

    def handle(self, *args: object, **options: object) -> None:
        """Виконує логіку `handle`.

Args:
    args: Вхідне значення для виконання операції.
    options: Вхідне значення для виконання операції.

Returns:
    None."""
        assign_group_permissions()
        self.stdout.write(self.style.SUCCESS('Roles created successfully'))
