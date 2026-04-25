"""Модуль `support_chat/views/operator.py` застосунку `support_chat`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from accounts.permissions import support_required
from support_chat.models import SupportChatSession, SupportChatStatus
from support_chat.services import assign_operator_to_chat


@login_required
@support_required
def operator_dashboard_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `operator_dashboard_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    waiting_sessions = SupportChatSession.objects.filter(
        status=SupportChatStatus.WAITING
    ).order_by("created_at")

    active_sessions = SupportChatSession.objects.filter(
        operator=request.user,
        status=SupportChatStatus.ACTIVE,
    ).order_by("-connected_at")

    return render(
        request,
        "avelon_healthcare/support_chat/pages/operator_dashboard.html",
        {
            "waiting_sessions": waiting_sessions,
            "active_sessions": active_sessions,
        },
    )


@login_required
@support_required
def operator_dashboard_data_view(request: HttpRequest) -> JsonResponse:
    """Виконує прикладну логіку функції `operator_dashboard_data_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        JsonResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    waiting_sessions = SupportChatSession.objects.filter(
        status=SupportChatStatus.WAITING
    )

    active_sessions = SupportChatSession.objects.filter(
        operator=request.user,
        status=SupportChatStatus.ACTIVE,
    )

    return JsonResponse(
        {
            "waiting_sessions": [
                {
                    "id": s.id,
                    "customer_display_name": s.customer_display_name,
                    "topic_display": s.get_topic_display(),
                    "initial_description": s.initial_description,
                    "created_at": s.created_at.strftime("%d.%m.%Y %H:%M"),
                }
                for s in waiting_sessions
            ],
            "active_sessions": [
                {
                    "id": s.id,
                    "customer_display_name": s.customer_display_name,
                    "topic_display": s.get_topic_display(),
                    "initial_description": s.initial_description,
                    "connected_at": s.connected_at.strftime("%d.%m.%Y %H:%M")
                    if s.connected_at else "",
                }
                for s in active_sessions
            ],
        }
    )


@require_POST
@login_required
@support_required
def claim_chat_view(request: HttpRequest, session_id: int) -> JsonResponse:
    """Виконує прикладну логіку функції `claim_chat_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        session_id: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        JsonResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    session = get_object_or_404(
        SupportChatSession,
        pk=session_id,
        status=SupportChatStatus.WAITING,
    )

    session = assign_operator_to_chat(session=session, operator=request.user)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"support_chat_{session.id}",
        {
            "type": "chat.event",
            "event_type": "operator_connected",
            "sender_role": "system",
            "sender_name": "",
            "text": f"До чату підключився оператор {session.operator_display_name}.",
        },
    )

    return JsonResponse({"ok": True, "session_id": session.id})


@login_required
@support_required
def operator_chat_room_view(request: HttpRequest, session_id: int) -> HttpResponse:
    """Виконує прикладну логіку функції `operator_chat_room_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        session_id: Значення типу `int`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    session = get_object_or_404(SupportChatSession, pk=session_id)

    return render(
        request,
        "avelon_healthcare/support_chat/pages/operator_chat_room.html",
        {
            "chat_session": session,
            "messages": session.messages.all(),
        },
    )
