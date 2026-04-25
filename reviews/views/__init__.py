"""Модуль `reviews/views/__init__.py` застосунку `reviews`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .public import review_list_view, review_create_view
from .support import support_review_list_view, support_review_reply_view

__all__ = [
    "review_list_view",
    "review_create_view",
    "support_review_list_view",
    "support_review_reply_view",
]
