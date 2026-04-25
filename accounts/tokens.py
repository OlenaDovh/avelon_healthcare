from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Генератор токенів для підтвердження електронної пошти.

    Формує токен на основі даних користувача та часу.
    """

    def _make_hash_value(self, user, timestamp: int) -> str:
        """
        Формує хеш для генерації токена.

        Args:
            user: Об'єкт користувача.
            timestamp: Часова мітка.

        Returns:
            str: Рядок для формування хешу токена.
        """
        return f"{user.pk}{user.email}{user.pending_email}{user.email_verified}{timestamp}"


email_verification_token = EmailVerificationTokenGenerator()
