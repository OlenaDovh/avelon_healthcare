"""Модуль `support_chat/views/__init__.py` застосунку `support_chat`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .public import (
    get_current_chat_session_view,
    create_chat_session_view,
    get_chat_session_view,
)

from .operator import (
    operator_dashboard_view,
    operator_dashboard_data_view,
    claim_chat_view,
    operator_chat_room_view,
)

__all__ = [
    "get_current_chat_session_view",
    "create_chat_session_view",
    "get_chat_session_view",
    "operator_dashboard_view",
    "operator_dashboard_data_view",
    "claim_chat_view",
    "operator_chat_room_view",
]
