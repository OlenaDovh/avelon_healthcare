from __future__ import annotations
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from core.utils.email import send_html_email


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def send_html_email_task(self, subject: str, html_body: str, to: list[str]) -> None:
    """
    Відправляє HTML email через Celery-задачу.

    Args:
        self: Екземпляр задачі Celery.
        subject: Тема листа.
        html_body: HTML-вміст листа.
        to: Список email-адрес отримувачів.

    Returns:
        None
    """
    send_html_email(
        subject=subject,
        html_body=html_body,
        to=to,
    )


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def send_password_reset_email_task(
        self,
        subject: str,
        body: str,
        from_email: str | None,
        to_email: str,
        html_email: str | None = None,
) -> None:
    """
    Відправляє лист для скидання пароля через Celery-задачу.

    Args:
        self: Екземпляр задачі Celery.
        subject: Тема листа.
        body: Текстовий вміст листа.
        from_email: Email відправника.
        to_email: Email отримувача.
        html_email: HTML-версія листа.

    Returns:
        None
    """
    message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[to_email],
    )

    if html_email:
        message.attach_alternative(html_email, "text/html")

    message.send()
