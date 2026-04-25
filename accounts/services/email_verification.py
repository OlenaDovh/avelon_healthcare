"""Модуль `accounts/services/email_verification.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tasks import send_html_email_task
from accounts.tokens import email_verification_token

User = get_user_model()


def build_email_verification_url(*, request: HttpRequest, user: User) -> str:
    """Виконує прикладну логіку функції `build_email_verification_url` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        user: Значення типу `User`, яке передається для виконання логіки функції.

    Повертає:
        str: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)

    return request.build_absolute_uri(
        reverse_lazy("accounts:verify_email", kwargs={"uidb64": uid, "token": token})
    )


def send_verification_email(
    *,
    request: HttpRequest,
    user: User,
    target_email: str,
    subject: str,
) -> None:
    """Виконує прикладну логіку функції `send_verification_email` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        user: Значення типу `User`, яке передається для виконання логіки функції.
        target_email: Значення типу `str`, яке передається для виконання логіки функції.
        subject: Значення типу `str`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    current_site = get_current_site(request)
    verify_url = build_email_verification_url(request=request, user=user)

    html_body = render_to_string(
        "avelon_healthcare/accounts/emails/email_verification_email.html",
        {
            "user": user,
            "verify_url": verify_url,
            "domain": current_site.domain,
        },
    )

    transaction.on_commit(
        lambda: send_html_email_task.delay(
            subject=subject,
            html_body=html_body,
            to=[target_email],
        )
    )
