"""Модуль `orders/services/__init__.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from .checkout import create_order_from_analyses
from .forms import get_order_form
from .invoice_pdf import build_order_invoice_response, generate_order_invoice_pdf
from .notifications import send_order_email
from .payments import (
    get_bank_transfer_auto_pay_after_minutes,
    update_bank_transfer_order_status,
    update_bank_transfer_orders_status,
)

__all__ = [
    "create_order_from_analyses",
    "get_order_form",
    "generate_order_invoice_pdf",
    "build_order_invoice_response",
    "send_order_email",
    "get_bank_transfer_auto_pay_after_minutes",
    "update_bank_transfer_order_status",
    "update_bank_transfer_orders_status",
]
