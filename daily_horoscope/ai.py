"""Модуль `daily_horoscope/ai.py` застосунку `daily_horoscope`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from django.conf import settings
import google.generativeai as genai

logger = logging.getLogger(__name__)

FALLBACK_TEXT = (
    "Сьогодні хороший день, щоб подбати про свій внутрішній баланс. "
    "Навіть кілька хвилин спокою, вода і м’який ритм дня допоможуть тобі відчути більше ресурсу."
)


def retry(max_attempts: int = 4, delay: float = 1.5, backoff: float = 2.0) -> Callable:
    """Виконує прикладну логіку функції `retry` у відповідному модулі проєкту.

    Параметри:
        max_attempts: Значення типу `int`, яке передається для виконання логіки функції.
        delay: Значення типу `float`, яке передається для виконання логіки функції.
        backoff: Значення типу `float`, яке передається для виконання логіки функції.

    Повертає:
        Callable: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    def decorator(func: Callable) -> Callable:
        """Виконує прикладну логіку функції `decorator` у відповідному модулі проєкту.

        Параметри:
            func: Значення типу `Callable`, яке передається для виконання логіки функції.

        Повертає:
            Callable: Результат роботи функції або обʼєкт, сформований під час виконання.
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Виконує прикладну логіку функції `wrapper` у відповідному модулі проєкту.

            Параметри:
                *args: Значення типу `Any`, яке передається для виконання логіки функції.
                **kwargs: Значення типу `Any`, яке передається для виконання логіки функції.

            Повертає:
                Any: Результат роботи функції або обʼєкт, сформований під час виконання.
            """
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    error_text = str(ex)

                    retryable = any(
                        marker in error_text
                        for marker in (
                            "503",
                            "429",
                            "UNAVAILABLE",
                            "RESOURCE_EXHAUSTED",
                            "INTERNAL",
                        )
                    )

                    if not retryable or attempt == max_attempts:
                        raise

                    logger.warning(
                        "Gemini attempt %s failed: %s. Retrying in %.1fs",
                        attempt,
                        ex,
                        current_delay,
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

            return None

        return wrapper

    return decorator


def _request_gemini_text(prompt: str) -> str:
    """Виконує прикладну логіку функції `_request_gemini_text` у відповідному модулі проєкту.

    Параметри:
        prompt: Значення типу `str`, яке передається для виконання логіки функції.

    Повертає:
        str: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if genai is None:
        raise RuntimeError("Gemini library not installed")

    if not settings.GEMINI_API_KEY:
        raise RuntimeError("Missing GEMINI_API_KEY")

    genai.configure(api_key=settings.GEMINI_API_KEY)

    model = genai.GenerativeModel(settings.GEMINI_MODEL)

    response = model.generate_content(prompt)

    text = (response.text or "").strip()
    if not text:
        raise ValueError("Gemini returned empty text.")

    return text


def generate_horoscope_text(theme: str, weekday: str) -> str:
    """Виконує прикладну логіку функції `generate_horoscope_text` у відповідному модулі проєкту.

    Параметри:
        theme: Значення типу `str`, яке передається для виконання логіки функції.
        weekday: Значення типу `str`, яке передається для виконання логіки функції.

    Повертає:
        str: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if not settings.GEMINI_API_KEY:
        return FALLBACK_TEXT

    prompt = f"""
Згенеруй короткий позитивний wellness-прогноз на день українською мовою.

Контекст:
- день тижня: {weekday}
- тема дня: {theme}

Вимоги:
- стиль теплий, м’який, підтримуючий
- 2-3 речення
- звертайся до читача на "ти"
- без містики
- без діагнозів
- без згадок про хвороби
- без медичних порад і лікування
- без залякування
- без негативних прогнозів
- акцент на самопочутті, балансі, турботі про себе, спокої, ресурсі

Поверни тільки готовий текст без заголовка і без лапок.
"""

    try:
        return _request_gemini_text(prompt)
    except Exception as exc:
        logger.exception("Gemini final error: %s", exc)
        return FALLBACK_TEXT
