from __future__ import annotations
from django.utils import timezone
from .models import SupportChatMessage, SupportChatSession, SupportChatStatus


def create_support_chat_session(
        *,
        user,
        guest_name: str,
        guest_email: str,
        topic: str,
        initial_description: str,
) -> SupportChatSession:
    """
    Створює нову сесію support-чату.

    Args:
        user: Авторизований користувач або None.
        guest_name: Ім'я гостя.
        guest_email: Email гостя.
        topic: Тема звернення.
        initial_description: Початковий опис звернення.

    Returns:
        SupportChatSession: Створена сесія чату.
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


def assign_operator_to_chat(
        *,
        session: SupportChatSession,
        operator,
) -> SupportChatSession:
    """
    Призначає оператора до сесії чату.

    Args:
        session: Сесія чату.
        operator: Користувач-оператор.

    Returns:
        SupportChatSession: Оновлена сесія чату.
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


def close_chat_session(
        *,
        session: SupportChatSession,
) -> SupportChatSession:
    """
    Закриває сесію support-чату.

    Args:
        session: Сесія чату.

    Returns:
        SupportChatSession: Оновлена сесія чату.
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
