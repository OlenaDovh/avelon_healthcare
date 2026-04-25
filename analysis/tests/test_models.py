from typing import Any
import pytest

@pytest.mark.django_db
def test_analysis_factory_creates_analysis(analysis: Any) -> None:
    """Виконує логіку `test_analysis_factory_creates_analysis`.

Args:
    analysis: Вхідний параметр `analysis`.

Returns:
    Any: Результат виконання."""
    assert analysis.id is not None
    assert analysis.name
    assert analysis.price is not None

@pytest.mark.django_db
def test_analysis_str_returns_name(analysis: Any) -> None:
    """Виконує логіку `test_analysis_str_returns_name`.

Args:
    analysis: Вхідний параметр `analysis`.

Returns:
    Any: Результат виконання."""
    assert str(analysis) == analysis.name
