"""Модуль support_chat/services.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
from django.utils import timezone
from .models import SupportChatMessage, SupportChatSession, SupportChatStatus


def create_support_chat_session(*, user: Any, guest_name: str, guest_email: str, topic: str,
                                initial_description: str) -> SupportChatSession:
    """Виконує логіку `create_support_chat_session`.

Args:
    user: Вхідне значення для виконання операції.
    guest_name: Вхідне значення для виконання операції.
    guest_email: Вхідне значення для виконання операції.
    topic: Вхідне значення для виконання операції.
    initial_description: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    session = SupportChatSession.objects.create(user=user, guest_name=guest_name, guest_email=guest_email, topic=topic,
                                                initial_description=initial_description)
    SupportChatMessage.objects.create(session=session, author_type=SupportChatMessage.AuthorType.SYSTEM, author_name='',
                                      text='Звернення створено. Очікуємо підключення оператора.')
    return session


def assign_operator_to_chat(*, session: SupportChatSession, operator: Any) -> SupportChatSession:
    """Виконує логіку `assign_operator_to_chat`.

Args:
    session: Вхідне значення для виконання операції.
    operator: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    session.operator = operator
    session.status = SupportChatStatus.ACTIVE
    session.connected_at = timezone.now()
    session.save(update_fields=['operator', 'status', 'connected_at'])
    SupportChatMessage.objects.create(session=session, author_type=SupportChatMessage.AuthorType.SYSTEM, author_name='',
                                      text=f'До чату підключився оператор {session.operator_display_name}.')
    return session


def close_chat_session(*, session: SupportChatSession) -> SupportChatSession:
    """Виконує логіку `close_chat_session`.

Args:
    session: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    if session.status != SupportChatStatus.CLOSED:
        session.status = SupportChatStatus.CLOSED
        session.closed_at = timezone.now()
        session.save(update_fields=['status', 'closed_at'])
        SupportChatMessage.objects.create(session=session, author_type=SupportChatMessage.AuthorType.SYSTEM,
                                          author_name='', text='Чат завершено.')
    return session
