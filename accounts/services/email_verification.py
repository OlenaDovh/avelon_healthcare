from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import email_verification_token
from core.utils.email import send_html_email

User = get_user_model()


def build_email_verification_url(*, request: HttpRequest, user: User) -> str:
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

    send_html_email(
        subject=subject,
        html_body=html_body,
        to=[target_email],
    )