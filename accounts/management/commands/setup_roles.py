from __future__ import annotations

from django.core.management.base import BaseCommand

from accounts.services import assign_group_permissions


class Command(BaseCommand):
    """
    Команда створення ролей і призначення дозволів.
    """

    help = "Create groups and assign permissions"

    def handle(self, *args: object, **options: object) -> None:
        """
        Виконує команду.

        Args:
            *args (object): Позиційні аргументи.
            **options (object): Іменовані аргументи.

        Returns:
            None
        """
        assign_group_permissions()
        self.stdout.write(self.style.SUCCESS("Roles created successfully"))