"""Модуль daily_horoscope/ai.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any
from django.conf import settings
import google.generativeai as genai
logger = logging.getLogger(__name__)
FALLBACK_TEXT = 'Сьогодні хороший день, щоб подбати про свій внутрішній баланс. Навіть кілька хвилин спокою, вода і м’який ритм дня допоможуть тобі відчути більше ресурсу.'

def retry(max_attempts: int=4, delay: float=1.5, backoff: float=2.0) -> Callable:
    """Виконує логіку `retry`.

Args:
    max_attempts: Вхідне значення для виконання операції.
    delay: Вхідне значення для виконання операції.
    backoff: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""

    def decorator(func: Callable) -> Callable:
        """Виконує логіку `decorator`.

Args:
    func: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Виконує логіку `wrapper`.

Args:
    args: Вхідне значення для виконання операції.
    kwargs: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    error_text = str(ex)
                    retryable = any((marker in error_text for marker in ('503', '429', 'UNAVAILABLE', 'RESOURCE_EXHAUSTED', 'INTERNAL')))
                    if not retryable or attempt == max_attempts:
                        raise
                    logger.warning('Gemini attempt %s failed: %s. Retrying in %.1fs', attempt, ex, current_delay)
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

def _request_gemini_text(prompt: str) -> str:
    """Виконує логіку `_request_gemini_text`.

Args:
    prompt: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    if genai is None:
        raise RuntimeError('Gemini library not installed')
    if not settings.GEMINI_API_KEY:
        raise RuntimeError('Missing GEMINI_API_KEY')
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    response = model.generate_content(prompt)
    text = (response.text or '').strip()
    if not text:
        raise ValueError('Gemini returned empty text.')
    return text

def generate_horoscope_text(theme: str, weekday: str) -> str:
    """Виконує логіку `generate_horoscope_text`.

Args:
    theme: Вхідне значення для виконання операції.
    weekday: Вхідне значення для виконання операції.

Returns:
    Результат виконання операції."""
    if not settings.GEMINI_API_KEY:
        return FALLBACK_TEXT
    prompt = f'\nЗгенеруй короткий позитивний wellness-прогноз на день українською мовою.\n\nКонтекст:\n- день тижня: {weekday}\n- тема дня: {theme}\n\nВимоги:\n- стиль теплий, м’який, підтримуючий\n- 2-3 речення\n- звертайся до читача на "ти"\n- без містики\n- без діагнозів\n- без згадок про хвороби\n- без медичних порад і лікування\n- без залякування\n- без негативних прогнозів\n- акцент на самопочутті, балансі, турботі про себе, спокої, ресурсі\n\nПоверни тільки готовий текст без заголовка і без лапок.\n'
    try:
        return _request_gemini_text(prompt)
    except Exception as exc:
        logger.exception('Gemini final error: %s', exc)
        return FALLBACK_TEXT
