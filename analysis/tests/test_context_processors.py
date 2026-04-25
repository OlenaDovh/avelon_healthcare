"""Модуль `analysis/tests/test_context_processors.py` застосунку `analysis`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
from analysis.context_processors import cart_items_count


def test_cart_items_count_returns_zero_for_empty_session(rf: Any) -> None:
    """Виконує прикладну логіку функції `test_cart_items_count_returns_zero_for_empty_session` у відповідному модулі проєкту.

    Параметри:
        rf: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    request = rf.get("/")
    request.session = {}

    result = cart_items_count(request)

    assert result == {"cart_items_count": 0}


def test_cart_items_count_returns_cart_length(rf: Any) -> None:
    """Виконує прикладну логіку функції `test_cart_items_count_returns_cart_length` у відповідному модулі проєкту.

    Параметри:
        rf: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    request = rf.get("/")
    request.session = {"cart": {"1": 1, "2": 1, "3": 1}}

    result = cart_items_count(request)

    assert result == {"cart_items_count": 3}
