from django.urls import path

from .consumers import SupportChatConsumer

websocket_urlpatterns = [
    path("ws/support-chat/<int:session_id>/", SupportChatConsumer.as_asgi()),
]