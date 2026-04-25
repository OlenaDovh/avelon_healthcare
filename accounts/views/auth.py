"""Модуль `accounts/views/auth.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from accounts.forms import LoginForm, RegisterForm
from accounts.permissions import is_staff_role
from accounts.services import send_verification_email
from accounts.tokens import email_verification_token

logger = logging.getLogger(__name__)
User = get_user_model()


def register_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `register_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.is_active = True
            user.save()

            send_verification_email(
                request=request,
                user=user,
                target_email=user.email,
                subject="Avelon Healthcare — підтвердження електронної пошти",
            )

            logger.info("Зареєстровано нового користувача: %s", user.username)
            messages.success(
                request,
                "Реєстрацію майже завершено. Підтвердіть електронну пошту за посиланням з листа.",
            )
            return redirect("accounts:login")

        logger.warning("Неуспішна спроба реєстрації користувача.")
    else:
        form = RegisterForm()

    return render(
        request,
        "avelon_healthcare/accounts/pages/register.html",
        {"form": form},
    )


def verify_email_view(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """Виконує прикладну логіку функції `verify_email_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.
        uidb64: Значення типу `str`, яке передається для виконання логіки функції.
        token: Значення типу `str`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    try:
        uid: str = force_str(urlsafe_base64_decode(uidb64))
        user: User | None = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        if user.pending_email:
            user.email = user.pending_email
            user.pending_email = ""

        user.email_verified = True
        user.save(update_fields=["email", "pending_email", "email_verified"])
        messages.success(request, "Електронну пошту підтверджено.")
    else:
        messages.error(request, "Посилання підтвердження недійсне або застаріле.")

    return redirect("accounts:login")


def login_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `login_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    if request.user.is_authenticated:
        if is_staff_role(request.user):
            return redirect("accounts:staff_dashboard")
        return redirect("accounts:profile")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)

            logger.info("Користувач увійшов у систему: %s", user.username)
            messages.success(request, "Ви успішно увійшли в систему.")

            if is_staff_role(user):
                return redirect("accounts:staff_dashboard")

            return redirect("accounts:profile")

        logger.warning("Неуспішна спроба входу в систему.")
    else:
        form = LoginForm()

    return render(
        request,
        "avelon_healthcare/accounts/pages/login.html",
        {"form": form},
    )


def logout_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `logout_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    username: str = request.user.username if request.user.is_authenticated else "anonymous"
    logger.info("Користувач вийшов із системи: %s", username)

    logout(request)
    messages.info(request, "Ви вийшли з акаунта.")
    return redirect("core:home")


def resend_verification_email_view(request: HttpRequest) -> HttpResponse:
    """Виконує прикладну логіку функції `resend_verification_email_view` у відповідному модулі проєкту.

    Параметри:
        request: Значення типу `HttpRequest`, яке передається для виконання логіки функції.

    Повертає:
        HttpResponse: Результат роботи функції або обʼєкт, сформований під час виконання.
    """
    user = request.user

    if not user.is_authenticated:
        return redirect("accounts:login")

    if not user.pending_email:
        messages.info(request, "Немає електронної пошти, що потребує підтвердження.")
        return redirect("accounts:profile")

    send_verification_email(
        request=request,
        user=user,
        target_email=user.pending_email,
        subject="Avelon Healthcare — підтвердження електронної пошти",
    )

    messages.success(request, "Лист підтвердження повторно надіслано.")
    return redirect("accounts:profile")
