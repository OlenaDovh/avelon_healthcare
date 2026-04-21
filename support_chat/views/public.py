from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from support_chat.forms import SupportChatGuestStartForm, SupportChatUserStartForm
from support_chat.models import SupportChatSession, SupportChatStatus
from support_chat.services import create_support_chat_session


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
                        "id": m.id,
                        "author_type": m.author_type,
                        "author_name": m.author_name,
                        "text": m.text,
                        "created_at": m.created_at.isoformat(),
                    }
                    for m in chat_session.messages.all()
                ],
            },
        }
    )


@require_POST
def create_chat_session_view(request: HttpRequest) -> JsonResponse:
    existing_session_id = request.session.get("support_chat_session_id")

    if existing_session_id:
        try:
            session = SupportChatSession.objects.get(pk=existing_session_id)
            if session.status != SupportChatStatus.CLOSED:
                return JsonResponse(
                    {
                        "ok": True,
                        "session_id": session.id,
                        "status": session.status,
                        "messages": [
                            {
                                "id": m.id,
                                "author_type": m.author_type,
                                "author_name": m.author_name,
                                "text": m.text,
                                "created_at": m.created_at.isoformat(),
                            }
                            for m in session.messages.all()
                        ],
                    }
                )
        except SupportChatSession.DoesNotExist:
            request.session.pop("support_chat_session_id", None)
            request.session.modified = True

    form = (
        SupportChatUserStartForm(request.POST)
        if request.user.is_authenticated
        else SupportChatGuestStartForm(request.POST)
    )

    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    if request.user.is_authenticated:
        session = create_support_chat_session(
            user=request.user,
            guest_name="",
            guest_email="",
            topic=form.cleaned_data["topic"],
            initial_description=form.cleaned_data["initial_description"],
        )
    else:
        session = create_support_chat_session(
            user=None,
            guest_name=form.cleaned_data["guest_name"],
            guest_email=form.cleaned_data["guest_email"],
            topic=form.cleaned_data["topic"],
            initial_description=form.cleaned_data["initial_description"],
        )

    request.session["support_chat_session_id"] = session.id
    request.session.modified = True

    return JsonResponse(
        {
            "ok": True,
            "session_id": session.id,
            "status": session.status,
            "messages": [
                {
                    "id": m.id,
                    "author_type": m.author_type,
                    "author_name": m.author_name,
                    "text": m.text,
                    "created_at": m.created_at.isoformat(),
                }
                for m in session.messages.all()
            ],
        }
    )


def get_chat_session_view(request: HttpRequest, session_id: int) -> JsonResponse:
    session = get_object_or_404(SupportChatSession, pk=session_id)

    return JsonResponse(
        {
            "id": session.id,
            "status": session.status,
            "operator_name": session.operator_display_name,
            "messages": [
                {
                    "id": m.id,
                    "author_type": m.author_type,
                    "author_name": m.author_name,
                    "text": m.text,
                    "created_at": m.created_at.isoformat(),
                }
                for m in session.messages.all()
            ],
        }
    )