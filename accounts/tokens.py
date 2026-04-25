"""Модуль accounts/tokens.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Клас EmailVerificationTokenGenerator.

Відповідає за поведінку, описану в цьому компоненті застосунку."""

    def _make_hash_value(self, user: Any, timestamp: Any) -> Any:
        """Виконує логіку `_make_hash_value`.

Args:
    user: Вхідне значення для виконання операції.
    timestamp: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
        return f'{user.pk}{user.email}{user.pending_email}{user.email_verified}{timestamp}'
email_verification_token = EmailVerificationTokenGenerator()
