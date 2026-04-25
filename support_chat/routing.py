"""Модуль support_chat/routing.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.urls import path
from .consumers import SupportChatConsumer

websocket_urlpatterns = [path('ws/support-chat/<int:session_id>/', SupportChatConsumer.as_asgi())]
