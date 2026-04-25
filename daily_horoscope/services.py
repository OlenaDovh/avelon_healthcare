"""Модуль `daily_horoscope/services.py` застосунку `daily_horoscope`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

import random
from django.http import HttpRequest
from django.utils import timezone

from daily_horoscope.ai import FALLBACK_TEXT, generate_horoscope_text

SESSION_KEY = "daily_horoscope"

HOROSCOPE_THEMES = [
    "енергія дня",
    "внутрішній баланс",
    "турбота про себе",
    "спокій і відновлення",
    "м’яка продуктивність",
    "емоційний комфорт",
    "гармонія і стабільність",
]


def get_or_create_daily_horoscope_for_session(request: HttpRequest) -> dict[str, str]:
    """Виконує прикладну логіку функції `get_or_create_daily_horoscope_for_session` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        dict[str, str]: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    today = timezone.localdate()
    today_str = today.strftime("%Y-%m-%d")

    if not request.session.session_key:
        request.session.save()

    horoscope_data = request.session.get(SESSION_KEY)

    if horoscope_data and horoscope_data.get("date") == today_str:
        return horoscope_data

    rng = random.Random(f"{today_str}-{request.session.session_key}")
    theme = rng.choice(HOROSCOPE_THEMES)
    weekday = today.strftime("%A")

    text = generate_horoscope_text(theme=theme, weekday=weekday)

    result = {
        "date": today_str,
        "text": text,
        "theme": theme,
    }

    request.session[SESSION_KEY] = result
    request.session.modified = True

    return result
