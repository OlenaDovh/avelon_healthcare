"""Модуль analysis/views/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .head_manager import head_manager_analysis_create_view, head_manager_analysis_list_view, head_manager_analysis_update_view
from .public import add_to_cart_view, analysis_list_view, cart_detail_view, remove_from_cart_view
