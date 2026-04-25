from __future__ import annotations

import pytest

from analysis.forms import AnalysisForm


def get_analysis_form_data(**overrides) -> dict:
    """
    Формує тестові дані для AnalysisForm.

    Returns:
        dict: Дані форми.
    """
    data: dict = {
        "name": "Загальний аналіз крові",
        "what_to_check": "Гемоглобін",
        "disease": "Анемія",
        "for_whom": "Для дорослих",
        "biomaterial": "Кров",
        "duration_days": 2,
        "price": "450.00",
        "is_active": True,
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_analysis_form_valid() -> None:
    """
    Перевіряє валідність AnalysisForm.
    """
    form: AnalysisForm = AnalysisForm(data=get_analysis_form_data())
    assert form.is_valid()