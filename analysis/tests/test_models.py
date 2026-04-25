from __future__ import annotations

import pytest


@pytest.mark.django_db
def test_analysis_factory_creates_analysis(analysis) -> None:
    """
    Перевіряє створення моделі Analysis через factory.
    """
    assert analysis.id is not None
    assert analysis.name
    assert analysis.price is not None


@pytest.mark.django_db
def test_analysis_str_returns_name(analysis) -> None:
    """
    Перевіряє строкове представлення Analysis.
    """
    assert str(analysis) == analysis.name