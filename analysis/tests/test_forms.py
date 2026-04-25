"""Модуль `analysis/tests/test_forms.py` застосунку `analysis`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest

from analysis.forms import AnalysisForm


def get_analysis_form_data(**overrides: Any) -> Any:
    """Виконує прикладну логіку функції `get_analysis_form_data` у відповідному модулі проєкту.

    Параметри:
        **overrides: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        Any: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    data = {
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
    """Виконує прикладну логіку функції `test_analysis_form_valid` у відповідному модулі проєкту.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    form = AnalysisForm(data=get_analysis_form_data())
    assert form.is_valid()
