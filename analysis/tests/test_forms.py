"""Модуль analysis/tests/test_forms.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
import pytest
from analysis.forms import AnalysisForm

def get_analysis_form_data(**overrides: Any) -> Any:
    """Виконує логіку `get_analysis_form_data`.

Args:
    overrides: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    data = {'name': 'Загальний аналіз крові', 'what_to_check': 'Гемоглобін', 'disease': 'Анемія', 'for_whom': 'Для дорослих', 'biomaterial': 'Кров', 'duration_days': 2, 'price': '450.00', 'is_active': True}
    data.update(overrides)
    return data

@pytest.mark.django_db
def test_analysis_form_valid() -> None:
    """Виконує логіку `test_analysis_form_valid`.

Returns:
    None."""
    form = AnalysisForm(data=get_analysis_form_data())
    assert form.is_valid()
