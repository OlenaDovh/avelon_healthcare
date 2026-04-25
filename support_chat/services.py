"""Модуль `support_chat/services.py` застосунку `support_chat`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations
from typing import Any

from django.utils import timezone

from .models import SupportChatMessage, SupportChatSession, SupportChatStatus


def create_support_chat_session(*, user: Any, guest_name: str, guest_email: str, topic: str, initial_description: str) -> SupportChatSession:
    """Виконує прикладну логіку функції `create_support_chat_session` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.
        guest_name: Значення типу `str`, яке передається для виконання логіки функції.
        guest_email: Значення типу `str`, яке передається для виконання логіки функції.
        topic: Значення типу `str`, яке передається для виконання логіки функції.
        initial_description: Значення типу `str`, яке передається для виконання логіки функції.

    Повертає:
        SupportChatSession: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    session = SupportChatSession.objects.create(
        user=user,
        guest_name=guest_name,
        guest_email=guest_email,
        topic=topic,
        initial_description=initial_description,
    )

    SupportChatMessage.objects.create(
        session=session,
        author_type=SupportChatMessage.AuthorType.SYSTEM,
        author_name="",
        text="Звернення створено. Очікуємо підключення оператора.",
    )

    return session


def assign_operator_to_chat(*, session: SupportChatSession, operator: Any) -> SupportChatSession:
    """Виконує прикладну логіку функції `assign_operator_to_chat` у відповідному модулі проєкту.

    Параметри:
        session: Значення типу `SupportChatSession`, яке передається для виконання логіки функції.
        operator: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        SupportChatSession: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    session.operator = operator
    session.status = SupportChatStatus.ACTIVE
    session.connected_at = timezone.now()
    session.save(update_fields=["operator", "status", "connected_at"])

    SupportChatMessage.objects.create(
        session=session,
        author_type=SupportChatMessage.AuthorType.SYSTEM,
        author_name="",
        text=f"До чату підключився оператор {session.operator_display_name}.",
    )

    return session


def close_chat_session(*, session: SupportChatSession) -> SupportChatSession:
    """Виконує прикладну логіку функції `close_chat_session` у відповідному модулі проєкту.

    Параметри:
        session: Значення типу `SupportChatSession`, яке передається для виконання логіки функції.

    Повертає:
        SupportChatSession: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if session.status != SupportChatStatus.CLOSED:
        session.status = SupportChatStatus.CLOSED
        session.closed_at = timezone.now()
        session.save(update_fields=["status", "closed_at"])

        SupportChatMessage.objects.create(
            session=session,
            author_type=SupportChatMessage.AuthorType.SYSTEM,
            author_name="",
            text="Чат завершено.",
        )

    return session
