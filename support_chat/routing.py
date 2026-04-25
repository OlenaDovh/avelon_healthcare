from __future__ import annotations
from django.urls import path
from django.urls.resolvers import URLPattern
from .consumers import SupportChatConsumer

"""
Маршрути WebSocket для support-чату.
"""

websocket_urlpatterns: list[URLPattern] = [
    path("ws/support-chat/<int:session_id>/", SupportChatConsumer.as_asgi()),
]
