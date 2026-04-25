"""Модуль accounts/tasks.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from core.utils.email import send_html_email

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 3})
def send_html_email_task(self, subject: str, html_body: str, to: list[str]) -> None:
    """Виконує логіку `send_html_email_task`.

Args:
    subject: Вхідне значення для виконання операції.
    html_body: Вхідне значення для виконання операції.
    to: Вхідне значення для виконання операції.

Returns:
    None."""
    send_html_email(subject=subject, html_body=html_body, to=to)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 3})
def send_password_reset_email_task(self, subject: str, body: str, from_email: str | None, to_email: str, html_email: str | None=None) -> None:
    """Виконує логіку `send_password_reset_email_task`.

Args:
    subject: Вхідне значення для виконання операції.
    body: Вхідне значення для виконання операції.
    from_email: Вхідне значення для виконання операції.
    to_email: Вхідне значення для виконання операції.
    html_email: Вхідне значення для виконання операції.

Returns:
    None."""
    message = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=[to_email])
    if html_email:
        message.attach_alternative(html_email, 'text/html')
    message.send()
