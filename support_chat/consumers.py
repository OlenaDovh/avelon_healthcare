from __future__ import annotations

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import SupportChatMessage, SupportChatSession, SupportChatStatus
from .services import close_chat_session


class SupportChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.room_group_name = f"support_chat_{self.session_id}"

        allowed = await self.is_allowed()
        if not allowed:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        event_type = content.get("type")

        if event_type == "message":
            text = (content.get("text") or "").strip()
            sender_role = content.get("sender_role")
            sender_name = content.get("sender_name") or ""

            if not text:
                return

            is_closed = await self.is_closed()
            if is_closed:
                return

            message = await self.save_message(sender_role, sender_name, text)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.event",
                    "event_type": "message",
                    "message_id": message["id"],
                    "sender_role": sender_role,
                    "sender_name": sender_name,
                    "text": text,
                    "created_at": message["created_at"],
                },
            )

        elif event_type == "typing_start":
            sender_role = content.get("sender_role")
            sender_name = content.get("sender_name") or ""

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.event",
                    "event_type": "typing_start",
                    "sender_role": sender_role,
                    "sender_name": sender_name,
                },
            )

        elif event_type == "typing_stop":
            sender_role = content.get("sender_role")
            sender_name = content.get("sender_name") or ""

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.event",
                    "event_type": "typing_stop",
                    "sender_role": sender_role,
                    "sender_name": sender_name,
                },
            )

        elif event_type == "close_chat":
            await self.close_chat()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.event",
                    "event_type": "closed",
                    "message_id": None,
                    "sender_role": "system",
                    "sender_name": "",
                    "text": "Чат завершено.",
                },
            )

    async def chat_event(self, event):
        await self.send_json(event)

    @database_sync_to_async
    def is_allowed(self) -> bool:
        try:
            session = SupportChatSession.objects.get(pk=self.session_id)
        except SupportChatSession.DoesNotExist:
            return False

        user = self.scope.get("user")
        if user and user.is_authenticated:
            if session.user_id == user.id:
                return True
            if session.operator_id == user.id:
                return True
            if user.is_staff:
                return True

        return True

    @database_sync_to_async
    def is_closed(self) -> bool:
        return SupportChatSession.objects.filter(
            pk=self.session_id,
            status=SupportChatStatus.CLOSED,
        ).exists()

    @database_sync_to_async
    def save_message(self, sender_role: str, sender_name: str, text: str) -> dict:
        session = SupportChatSession.objects.get(pk=self.session_id)

        author_type = SupportChatMessage.AuthorType.USER
        if sender_role == "operator":
            author_type = SupportChatMessage.AuthorType.OPERATOR
        elif sender_role == "system":
            author_type = SupportChatMessage.AuthorType.SYSTEM

        message = SupportChatMessage.objects.create(
            session=session,
            author_type=author_type,
            author_name=sender_name,
            text=text,
        )

        return {
            "id": message.id,
            "created_at": message.created_at.isoformat(),
        }

    @database_sync_to_async
    def close_chat(self) -> None:
        session = SupportChatSession.objects.get(pk=self.session_id)
        close_chat_session(session=session)