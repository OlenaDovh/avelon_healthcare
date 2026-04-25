from __future__ import annotations
from typing import Any
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Описує клас `EmailVerificationTokenGenerator`."""

    def _make_hash_value(self, user: Any, timestamp: Any) -> Any:
        """Виконує логіку `_make_hash_value`.

Args:
    user: Вхідний параметр `user`.
    timestamp: Вхідний параметр `timestamp`.

Returns:
    Any: Результат виконання."""
        return f'{user.pk}{user.email}{user.pending_email}{user.email_verified}{timestamp}'
email_verification_token = EmailVerificationTokenGenerator()
