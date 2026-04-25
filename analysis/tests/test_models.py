"""Модуль `analysis/tests/test_models.py` застосунку `analysis`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest


@pytest.mark.django_db
def test_analysis_factory_creates_analysis(analysis: Any) -> None:
    """Виконує прикладну логіку функції `test_analysis_factory_creates_analysis` у відповідному модулі проєкту.

    Параметри:
        analysis: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    assert analysis.id is not None
    assert analysis.name
    assert analysis.price is not None


@pytest.mark.django_db
def test_analysis_str_returns_name(analysis: Any) -> None:
    """Виконує прикладну логіку функції `test_analysis_str_returns_name` у відповідному модулі проєкту.

    Параметри:
        analysis: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    assert str(analysis) == analysis.name
