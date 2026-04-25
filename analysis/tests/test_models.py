"""Модуль analysis/tests/test_models.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest

@pytest.mark.django_db
def test_analysis_factory_creates_analysis(analysis: Any) -> None:
    """Виконує логіку `test_analysis_factory_creates_analysis`.

Args:
    analysis: Вхідне значення для виконання операції.

Returns:
    None."""
    assert analysis.id is not None
    assert analysis.name
    assert analysis.price is not None

@pytest.mark.django_db
def test_analysis_str_returns_name(analysis: Any) -> None:
    """Виконує логіку `test_analysis_str_returns_name`.

Args:
    analysis: Вхідне значення для виконання операції.

Returns:
    None."""
    assert str(analysis) == analysis.name
