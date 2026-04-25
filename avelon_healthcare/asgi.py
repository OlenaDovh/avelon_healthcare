"""Модуль avelon_healthcare/asgi.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avelon_healthcare.settings.local')
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import support_chat.routing
application = ProtocolTypeRouter({'http': django_asgi_app, 'websocket': AuthMiddlewareStack(URLRouter(support_chat.routing.websocket_urlpatterns))})
