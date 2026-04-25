"""Модуль reviews/views/__init__.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from .public import review_list_view, review_create_view
from .support import support_review_list_view, support_review_reply_view
__all__ = ['review_list_view', 'review_create_view', 'support_review_list_view', 'support_review_reply_view']
