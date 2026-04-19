from __future__ import annotations

import random

from django.utils import timezone

from .ai import FALLBACK_TEXT, generate_horoscope_text

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


def get_or_create_daily_horoscope_for_session(request) -> dict[str, str]:
    today = timezone.localdate()
    today_str = today.strftime("%Y-%m-%d")

    if not request.session.session_key:
        request.session.save()

    horoscope_data = request.session.get(SESSION_KEY)

    if horoscope_data and horoscope_data.get("date") == today_str:
        return horoscope_data

    seed_value = f"{today_str}-{request.session.session_key}"
    random.seed(seed_value)

    theme = random.choice(HOROSCOPE_THEMES)
    weekday = today.strftime("%A")

    text = generate_horoscope_text(theme=theme, weekday=weekday)

    result = {
        "date": today_str,
        "text": text,
        "theme": theme,
    }

    if text != FALLBACK_TEXT:
        request.session[SESSION_KEY] = result
        request.session.modified = True

    return result