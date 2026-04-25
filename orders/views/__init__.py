"""Модуль `orders/views/__init__.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .patient import (
    order_cancel_view,
    order_detail_view,
    order_invoice_view,
    order_list_view,
    order_pay_view,
)
from .public import order_create_view
from .support import (
    support_order_create_view,
    support_order_list_view,
    support_order_update_view,
)
