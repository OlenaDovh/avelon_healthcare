from __future__ import annotations

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from accounts.permissions import support_required
from .forms import SupportChatGuestStartForm, SupportChatUserStartForm
from .models import SupportChatSession, SupportChatStatus
from .services import assign_operator_to_chat, create_support_chat_session


def get_current_chat_session_view(request: HttpRequest) -> JsonResponse:
    session_id = request.session.get("support_chat_session_id")

    if not session_id:
        return JsonResponse({"ok": True, "session": None})

    try:
        chat_session = SupportChatSession.objects.get(pk=session_id)
    except SupportChatSession.DoesNotExist:
        request.session.pop("support_chat_session_id", None)
        request.session.modified = True
        return JsonResponse({"ok": True, "session": None})

    if chat_session.status == SupportChatStatus.CLOSED:
        request.session.pop("support_chat_session_id", None)
        request.session.modified = True
        return JsonResponse({"ok": True, "session": None})

    return JsonResponse(
        {
            "ok": True,
            "session": {
                "id": chat_session.id,
                "status": chat_session.status,
                "operator_name": chat_session.operator_display_name,
                "messages": [
                    {
                        "id": message.id,
                        "author_type": message.author_type,
                        "author_name": message.author_name,
                        "text": message.text,
                        "created_at": message.created_at.isoformat(),
                    }
                    for message in chat_session.messages.all()
                ],
            },
        }
    )


@require_POST
def create_chat_session_view(request: HttpRequest) -> JsonResponse:
    existing_session_id = request.session.get("support_chat_session_id")
    if existing_session_id:
        try:
            existing_session = SupportChatSession.objects.get(pk=existing_session_id)
            if existing_session.status != SupportChatStatus.CLOSED:
                return JsonResponse(
                    {
                        "ok": True,
                        "session_id": existing_session.id,
                        "status": existing_session.status,
                        "messages": [
                            {
                                "id": message.id,
                                "author_type": message.author_type,
                                "author_name": message.author_name,
                                "text": message.text,
                                "created_at": message.created_at.isoformat(),
                            }
                            for message in existing_session.messages.all()
                        ],
                    }
                )
        except SupportChatSession.DoesNotExist:
            request.session.pop("support_chat_session_id", None)
            request.session.modified = True

    if request.user.is_authenticated:
        form = SupportChatUserStartForm(request.POST)
    else:
        form = SupportChatGuestStartForm(request.POST)

    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    if request.user.is_authenticated:
        chat_session = create_support_chat_session(
            user=request.user,
            guest_name="",
            guest_email="",
            topic=form.cleaned_data["topic"],
            initial_description=form.cleaned_data["initial_description"],
        )
    else:
        chat_session = create_support_chat_session(
            user=None,
            guest_name=form.cleaned_data["guest_name"],
            guest_email=form.cleaned_data["guest_email"],
            topic=form.cleaned_data["topic"],
            initial_description=form.cleaned_data["initial_description"],
        )

    request.session["support_chat_session_id"] = chat_session.id
    request.session.modified = True

    return JsonResponse(
        {
            "ok": True,
            "session_id": chat_session.id,
            "status": chat_session.status,
            "messages": [
                {
                    "id": message.id,
                    "author_type": message.author_type,
                    "author_name": message.author_name,
                    "text": message.text,
                    "created_at": message.created_at.isoformat(),
                }
                for message in chat_session.messages.all()
            ],
        }
    )


def get_chat_session_view(request: HttpRequest, session_id: int) -> JsonResponse:
    chat_session = get_object_or_404(SupportChatSession, pk=session_id)

    return JsonResponse(
        {
            "id": chat_session.id,
            "status": chat_session.status,
            "operator_name": chat_session.operator_display_name,
            "messages": [
                {
                    "id": message.id,
                    "author_type": message.author_type,
                    "author_name": message.author_name,
                    "text": message.text,
                    "created_at": message.created_at.isoformat(),
                }
                for message in chat_session.messages.all()
            ],
        }
    )


@login_required
@support_required
def operator_dashboard_view(request: HttpRequest) -> HttpResponse:
    waiting_sessions = SupportChatSession.objects.filter(
        status=SupportChatStatus.WAITING
    ).order_by("created_at")

    active_sessions = SupportChatSession.objects.filter(
        operator=request.user,
        status=SupportChatStatus.ACTIVE,
    ).order_by("-connected_at")

    return render(
        request,
        "avelon_healthcare/support_chat/operator_dashboard.html",
        {
            "waiting_sessions": waiting_sessions,
            "active_sessions": active_sessions,
        },
    )


@login_required
@support_required
def operator_dashboard_data_view(request: HttpRequest) -> JsonResponse:
    waiting_sessions = SupportChatSession.objects.filter(
        status=SupportChatStatus.WAITING
    ).order_by("created_at")

    active_sessions = SupportChatSession.objects.filter(
        operator=request.user,
        status=SupportChatStatus.ACTIVE,
    ).order_by("-connected_at")

    return JsonResponse(
        {
            "waiting_sessions": [
                {
                    "id": session.id,
                    "customer_display_name": session.customer_display_name,
                    "topic_display": session.get_topic_display(),
                    "initial_description": session.initial_description,
                    "created_at": session.created_at.strftime("%d.%m.%Y %H:%M"),
                }
                for session in waiting_sessions
            ],
            "active_sessions": [
                {
                    "id": session.id,
                    "customer_display_name": session.customer_display_name,
                    "topic_display": session.get_topic_display(),
                    "initial_description": session.initial_description,
                    "connected_at": session.connected_at.strftime("%d.%m.%Y %H:%M")
                    if session.connected_at
                    else "",
                }
                for session in active_sessions
            ],
        }
    )


@require_POST
@login_required
@support_required
def claim_chat_view(request: HttpRequest, session_id: int) -> JsonResponse:
    chat_session = get_object_or_404(
        SupportChatSession,
        pk=session_id,
        status=SupportChatStatus.WAITING,
    )

    chat_session = assign_operator_to_chat(session=chat_session, operator=request.user)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"support_chat_{chat_session.id}",
        {
            "type": "chat.event",
            "event_type": "operator_connected",
            "sender_role": "system",
            "sender_name": "",
            "text": f"До чату підключився оператор {chat_session.operator_display_name}.",
        },
    )

    return JsonResponse({"ok": True, "session_id": chat_session.id})


@login_required
@support_required
def operator_chat_room_view(request: HttpRequest, session_id: int) -> HttpResponse:
    chat_session = get_object_or_404(SupportChatSession, pk=session_id)

    return render(
        request,
        "avelon_healthcare/support_chat/operator_chat_room.html",
        {
            "chat_session": chat_session,
            "messages": chat_session.messages.all(),
        },
    )