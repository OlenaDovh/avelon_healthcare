"""Модуль orders/views/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .patient import order_cancel_view, order_detail_view, order_invoice_view, order_list_view, order_pay_view
from .public import order_create_view
from .support import support_order_create_view, support_order_list_view, support_order_update_view
