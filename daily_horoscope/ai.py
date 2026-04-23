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
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
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


@retry()
def _request_gemini_text(prompt: str) -> str:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    text = (response.text or "").strip()
    if not text:
        raise ValueError("Gemini returned empty text.")

    return text


def generate_horoscope_text(theme: str, weekday: str) -> str:
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