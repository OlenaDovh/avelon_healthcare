"""Модуль `support_chat/routing.py` застосунку `support_chat`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from django.urls import path

from .consumers import SupportChatConsumer

websocket_urlpatterns = [
    path("ws/support-chat/<int:session_id>/", SupportChatConsumer.as_asgi()),
]
