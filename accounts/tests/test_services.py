"""Модуль `accounts/tests/test_services.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from typing import Any
import pytest
from django.test import RequestFactory

from unittest.mock import patch

from accounts.services import build_email_verification_url, send_verification_email


@pytest.mark.django_db
def test_build_email_verification_url_returns_absolute_url(user: Any) -> None:
    """Виконує прикладну логіку функції `test_build_email_verification_url_returns_absolute_url` у відповідному модулі проєкту.

    Параметри:
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    request = RequestFactory().get("/")
    request.META["HTTP_HOST"] = "testserver"

    url = build_email_verification_url(request=request, user=user)

    assert url.startswith("http://testserver")
    assert "/verify-email/" in url


@pytest.mark.django_db
@patch("accounts.services.email_verification.send_html_email")
def test_send_verification_email_calls_send_html_email(mock_send_html_email: Any, user: Any) -> None:
    """Виконує прикладну логіку функції `test_send_verification_email_calls_send_html_email` у відповідному модулі проєкту.

    Параметри:
        mock_send_html_email: Значення типу `Any`, яке передається для виконання логіки функції.
        user: Значення типу `Any`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    request = RequestFactory().get("/")
    request.META["HTTP_HOST"] = "testserver"

    send_verification_email(
        request=request,
        user=user,
        target_email="target@example.com",
        subject="Verify email",
    )

    mock_send_html_email.assert_called_once()
    _, kwargs = mock_send_html_email.call_args
    assert kwargs["subject"] == "Verify email"
    assert kwargs["to"] == ["target@example.com"]
    assert "html_body" in kwargs
