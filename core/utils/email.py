"""Модуль `core/utils/email.py` застосунку `core`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

# core/utils/email.py
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
    """Виконує прикладну логіку функції `send_html_email` у відповідному модулі проєкту.

    Параметри:
        subject: Значення типу `str`, яке передається для виконання логіки функції.
        html_body: Значення типу `str`, яке передається для виконання логіки функції.
        to: Значення типу `list[str]`, яке передається для виконання логіки функції.
        attachments: Значення типу `list[tuple[str, bytes, str]] | None`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    text_body: str = strip_tags(html_body)

    email = EmailMultiAlternatives(
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
