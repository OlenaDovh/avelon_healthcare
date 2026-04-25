from django.core.management.base import BaseCommand
from accounts.services import assign_group_permissions


class Command(BaseCommand):
    """
    Команда створення ролей і призначення дозволів.

    Викликає сервіс для створення груп та налаштування їх прав доступу.
    """

    help = "Create groups and assign permissions"

    def handle(self, *args: object, **options: object) -> None:
        """
        Виконує команду створення ролей та призначення дозволів.

        Args:
            *args: Позиційні аргументи.
            **options: Іменовані аргументи.
        """
        assign_group_permissions()
        self.stdout.write(self.style.SUCCESS("Roles created successfully"))
