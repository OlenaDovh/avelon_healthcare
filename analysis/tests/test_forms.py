from typing import Any
import pytest
from analysis.forms import AnalysisForm

def get_analysis_form_data(**overrides: Any) -> Any:
    """Виконує логіку `get_analysis_form_data`.

Args:
    **overrides: Вхідний параметр `overrides`.

Returns:
    Any: Результат виконання."""
    data = {'name': 'Загальний аналіз крові', 'what_to_check': 'Гемоглобін', 'disease': 'Анемія', 'for_whom': 'Для дорослих', 'biomaterial': 'Кров', 'duration_days': 2, 'price': '450.00', 'is_active': True}
    data.update(overrides)
    return data

@pytest.mark.django_db
def test_analysis_form_valid() -> None:
    """Виконує логіку `test_analysis_form_valid`.

Returns:
    Any: Результат виконання."""
    form = AnalysisForm(data=get_analysis_form_data())
    assert form.is_valid()
