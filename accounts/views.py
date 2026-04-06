from __future__ import annotations
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from .forms import (
    LoginForm,
    ProfileUpdateForm,
    RegisterForm,
    UserPasswordChangeForm,
    UserPasswordResetForm,
)

import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm

logger = logging.getLogger(__name__)


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає та обробляє форму реєстрації користувача.

    Після успішної реєстрації користувач автоматично входить у систему
    та перенаправляється до особистого кабінету.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь або редірект.
    """
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.save()

            logger.info("Зареєстровано нового користувача: %s", user.username)

            login(request, user, backend='accounts.backends.EmailOrUsernameBackend')
            messages.success(request, "Реєстрація пройшла успішно.")
            return redirect("accounts:profile")

        logger.warning("Неуспішна спроба реєстрації користувача.")
    else:
        form = RegisterForm()

    return render(
        request,
        "avelon_healthcare/accounts/register.html",
        {"form": form},
    )


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає та обробляє форму входу користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь або редірект.
    """
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)

            logger.info("Користувач увійшов у систему: %s", user.username)

            messages.success(request, "Ви успішно увійшли в систему.")
            return redirect("accounts:profile")

        logger.warning("Неуспішна спроба входу в систему.")
    else:
        form = LoginForm()

    return render(
        request,
        "avelon_healthcare/accounts/login.html",
        {"form": form},
    )


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Виконує вихід користувача із системи.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: Редірект на головну сторінку.
    """
    username: str = request.user.username if request.user.is_authenticated else "anonymous"
    logger.info("Користувач вийшов із системи: %s", username)

    logout(request)
    messages.info(request, "Ви вийшли з акаунта.")
    return redirect("core:home")


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає сторінку особистого кабінету користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь зі сторінкою профілю.
    """
    return render(request, "avelon_healthcare/accounts/profile.html")

@login_required
def profile_update_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає та обробляє форму редагування профілю користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь або редірект.
    """
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            logger.info("Оновлено профіль користувача: %s", request.user.username)
            messages.success(request, "Профіль успішно оновлено.")
            return redirect("accounts:profile")

        logger.warning(
            "Неуспішна спроба оновлення профілю. user=%s",
            request.user.username,
        )
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(
        request,
        "avelon_healthcare/accounts/profile_update.html",
        {"form": form},
    )

@login_required
def password_change_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає та обробляє форму зміни пароля користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь або редірект.
    """
    if request.method == "POST":
        form = UserPasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            logger.info("Користувач змінив пароль: %s", request.user.username)
            messages.success(request, "Пароль успішно змінено.")
            return redirect("accounts:profile")

        logger.warning(
            "Неуспішна спроба зміни пароля. user=%s",
            request.user.username,
        )
    else:
        form = UserPasswordChangeForm(user=request.user)

    return render(
        request,
        "avelon_healthcare/accounts/password_change.html",
        {"form": form},
    )

class UserPasswordResetView(PasswordResetView):
    """
    Представлення для відновлення пароля через email.

    Використовує кастомну форму і шаблони,
    а також записує подію в лог.
    """

    form_class = UserPasswordResetForm
    template_name = "avelon_healthcare/accounts/password_reset_form.html"
    email_template_name = "avelon_healthcare/accounts/password_reset_email.txt"
    subject_template_name = "avelon_healthcare/accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")

    def form_valid(self, form: UserPasswordResetForm) -> HttpResponse:
        """
        Обробляє валідну форму відновлення пароля.

        Args:
            form (UserPasswordResetForm): Валідна форма.

        Returns:
            HttpResponse: Редірект на сторінку успішного відправлення листа.
        """
        logger.info(
            "Запит на відновлення пароля для email=%s",
            form.cleaned_data.get("email"),
        )
        return super().form_valid(form)