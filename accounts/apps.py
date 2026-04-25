from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Конфігурація застосунку accounts.

    Визначає налаштування та ініціалізацію застосунку.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self) -> None:
        """
        Виконує ініціалізацію застосунку та підключає сигнали.

        Returns:
            None
        """
        import accounts.signals