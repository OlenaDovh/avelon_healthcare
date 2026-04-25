"""Модуль support_chat/models.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations

from django.conf import settings
from django.db import models


class SupportChatStatus(models.TextChoices):
    """Клас SupportChatStatus.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    WAITING = "waiting", "Очікує оператора"
    ACTIVE = "active", "Активний"
    CLOSED = "closed", "Завершений"


class SupportChatTopic(models.TextChoices):
    """Клас SupportChatTopic.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    APPOINTMENT = "appointment", "Запис на прийом"
    ANALYSIS = "analysis", "Аналізи"
    ORDER = "order", "Замовлення"
    ACCOUNT = "account", "Акаунт"
    OTHER = "other", "Інше"


class SupportChatSession(models.Model):
    """Клас SupportChatSession.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="support_chat_sessions",
        verbose_name="Користувач",
    )
    guest_name = models.CharField(max_length=150, blank=True, verbose_name="Ім'я гостя")
    guest_email = models.EmailField(blank=True, verbose_name="Email гостя")

    topic = models.CharField(
        max_length=50,
        choices=SupportChatTopic.choices,
        verbose_name="Тема звернення",
    )
    initial_description = models.TextField(verbose_name="Опис звернення")

    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_support_chat_sessions",
        verbose_name="Оператор",
    )

    status = models.CharField(
        max_length=20,
        choices=SupportChatStatus.choices,
        default=SupportChatStatus.WAITING,
        verbose_name="Статус",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    connected_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        ordering = ["-created_at"]
        verbose_name = "Сесія чату підтримки"
        verbose_name_plural = "Сесії чату підтримки"

    @property
    def customer_display_name(self) -> str:
        """Виконує логіку `customer_display_name`.

Returns:
    Результат виконання операції."""
        if self.user:
            return self.user.full_name or self.user.username
        return self.guest_name or "Гість"

    @property
    def operator_display_name(self) -> str:
        """Виконує логіку `operator_display_name`.

Returns:
    Результат виконання операції."""
        if not self.operator:
            return ""
        return self.operator.full_name or self.operator.username

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return f"Чат #{self.pk} — {self.customer_display_name}"


class SupportChatMessage(models.Model):
    """Клас SupportChatMessage.

Відповідає за поведінку, описану в цьому компоненті застосунку."""

    class AuthorType(models.TextChoices):
        """Клас AuthorType.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        USER = "user", "Користувач"
        OPERATOR = "operator", "Оператор"
        SYSTEM = "system", "Система"

    session = models.ForeignKey(
        SupportChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Сесія",
    )
    author_type = models.CharField(max_length=20, choices=AuthorType.choices)
    author_name = models.CharField(max_length=150, blank=True)
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        ordering = ["created_at"]
        verbose_name = "Повідомлення чату"
        verbose_name_plural = "Повідомлення чату"

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return f"{self.author_type}: {self.text[:40]}"
