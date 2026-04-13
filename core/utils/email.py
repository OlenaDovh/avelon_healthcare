from __future__ import annotations

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def send_html_email(
    *,
    subject: str,
    html_body: str,
    to: list[str],
    attachments: list[tuple[str, bytes, str]] | None = None,
) -> None:
    """
    Надсилає HTML-лист.

    Args:
        subject (str): Тема листа.
        html_body (str): HTML-вміст листа.
        to (list[str]): Список отримувачів.
        attachments (list[tuple[str, bytes, str]] | None): Вкладення.

    Returns:
        None
    """
    text_body: str = strip_tags(html_body)

    email: EmailMultiAlternatives = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to,
    )
    email.attach_alternative(html_body, "text/html")

    if attachments:
        for filename, content, mimetype in attachments:
            email.attach(filename=filename, content=content, mimetype=mimetype)

    email.send(fail_silently=True)