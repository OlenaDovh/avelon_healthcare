from typing import Any
import pytest
from django.test import RequestFactory
from unittest.mock import patch
from accounts.services import build_email_verification_url, send_verification_email

@pytest.mark.django_db
def test_build_email_verification_url_returns_absolute_url(user: Any) -> None:
    """Виконує логіку `test_build_email_verification_url_returns_absolute_url`.

Args:
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    request = RequestFactory().get('/')
    request.META['HTTP_HOST'] = 'testserver'
    url = build_email_verification_url(request=request, user=user)
    assert url.startswith('http://testserver')
    assert '/verify-email/' in url

@pytest.mark.django_db
@patch('accounts.services.email_verification.send_html_email')
def test_send_verification_email_calls_send_html_email(mock_send_html_email: Any, user: Any) -> None:
    """Виконує логіку `test_send_verification_email_calls_send_html_email`.

Args:
    mock_send_html_email: Вхідний параметр `mock_send_html_email`.
    user: Вхідний параметр `user`.

Returns:
    Any: Результат виконання."""
    request = RequestFactory().get('/')
    request.META['HTTP_HOST'] = 'testserver'
    send_verification_email(request=request, user=user, target_email='target@example.com', subject='Verify email')
    mock_send_html_email.assert_called_once()
    _, kwargs = mock_send_html_email.call_args
    assert kwargs['subject'] == 'Verify email'
    assert kwargs['to'] == ['target@example.com']
    assert 'html_body' in kwargs
