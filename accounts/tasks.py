from __future__ import annotations
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from core.utils.email import send_html_email

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 3})
def send_html_email_task(self, subject: str, html_body: str, to: list[str]) -> None:
    """Виконує логіку `send_html_email_task`.

Args:
    subject: Вхідний параметр `subject`.
    html_body: Вхідний параметр `html_body`.
    to: Вхідний параметр `to`.

Returns:
    Any: Результат виконання."""
    send_html_email(subject=subject, html_body=html_body, to=to)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 3})
def send_password_reset_email_task(self, subject: str, body: str, from_email: str | None, to_email: str, html_email: str | None=None) -> None:
    """Виконує логіку `send_password_reset_email_task`.

Args:
    subject: Вхідний параметр `subject`.
    body: Вхідний параметр `body`.
    from_email: Вхідний параметр `from_email`.
    to_email: Вхідний параметр `to_email`.
    html_email: Вхідний параметр `html_email`.

Returns:
    Any: Результат виконання."""
    message = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=[to_email])
    if html_email:
        message.attach_alternative(html_email, 'text/html')
    message.send()
