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
from django.shortcuts import redirect, render, get_object_or_404

from .forms import LoginForm, RegisterForm
from .permissions import is_staff_role

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from core.utils.email import send_html_email
from .tokens import email_verification_token

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from .forms import SupportPatientUpdateForm
from .permissions import support_required

logger = logging.getLogger(__name__)

User = get_user_model()

PATIENT_GROUP_NAME: str = "patient"


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає та обробляє форму реєстрації користувача.

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
            user.is_active = True
            user.save()

            current_site = get_current_site(request)
            uid: str = urlsafe_base64_encode(force_bytes(user.pk))
            token: str = email_verification_token.make_token(user)
            verify_url: str = request.build_absolute_uri(
                reverse_lazy("accounts:verify_email", kwargs={"uidb64": uid, "token": token})
            )

            html_body: str = render_to_string(
                "avelon_healthcare/accounts/email_verification_email.html",
                {
                    "user": user,
                    "verify_url": verify_url,
                    "domain": current_site.domain,
                },
            )

            send_html_email(
                subject="Avelon Healthcare — підтвердження електронної пошти",
                html_body=html_body,
                to=[user.email],
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
        "avelon_healthcare/accounts/register.html",
        {"form": form},
    )


def verify_email_view(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """
    Підтверджує електронну пошту користувача.
    Якщо є pending_email — робить її основною.
    """
    try:
        uid: str = force_str(urlsafe_base64_decode(uidb64))
        user: User = User.objects.get(pk=uid)
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
    """
    Відображає та обробляє форму входу користувача.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь або редірект.
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
    Редагування профілю.
    Якщо користувач змінює email, нова адреса йде в pending_email
    і потребує підтвердження.
    """
    if request.method == "POST":
        current_email: str = request.user.email
        form = ProfileUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)
            requested_email: str = form.cleaned_data["email"]

            email_changed: bool = current_email.lower() != requested_email.lower()

            if email_changed:
                user.pending_email = requested_email
                user.email_verified = False
                user.email = current_email
            else:
                if not user.pending_email:
                    user.email_verified = True

            user.save()

            if email_changed:
                current_site = get_current_site(request)
                uid: str = urlsafe_base64_encode(force_bytes(user.pk))
                token: str = email_verification_token.make_token(user)
                verify_url: str = request.build_absolute_uri(
                    reverse_lazy("accounts:verify_email", kwargs={"uidb64": uid, "token": token})
                )

                html_body: str = render_to_string(
                    "avelon_healthcare/accounts/email_verification_email.html",
                    {
                        "user": user,
                        "verify_url": verify_url,
                        "domain": current_site.domain,
                    },
                )

                send_html_email(
                    subject="Avelon Healthcare — підтвердження нової електронної пошти",
                    html_body=html_body,
                    to=[user.pending_email],
                )

                logger.info(
                    "Користувач ініціював зміну email. user=%s pending_email=%s",
                    request.user.username,
                    user.pending_email,
                )
                messages.warning(
                    request,
                    "Ми надіслали лист для підтвердження нової електронної пошти. "
                    "Поточна адреса залишиться активною, доки ви не підтвердите нову."
                )
            else:
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

    @login_required
    def staff_dashboard_view(self, request: HttpRequest) -> HttpResponse:
        """
        Відображає staff dashboard.

        Args:
            request (HttpRequest): HTTP-запит користувача.

        Returns:
            HttpResponse: HTML-відповідь.
        """
        if not is_staff_role(request.user):
            return redirect("accounts:profile")

        return render(
            request,
            "avelon_healthcare/accounts/staff_dashboard.html",
        )


@login_required
def staff_dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає staff dashboard.

    Args:
        request (HttpRequest): HTTP-запит користувача.

    Returns:
        HttpResponse: HTML-відповідь.
    """
    if not is_staff_role(request.user):
        return redirect("accounts:profile")

    return render(
        request,
        "avelon_healthcare/accounts/staff_dashboard.html",
    )


@login_required
@support_required
def support_patient_list_view(request: HttpRequest) -> HttpResponse:
    """
    Відображає список усіх пацієнтів для support.

    Args:
        request (HttpRequest): HTTP-запит.

    Returns:
        HttpResponse: HTML-відповідь.
    """
    patients = User.objects.filter(
        groups__name=PATIENT_GROUP_NAME,
    ).order_by("last_name", "first_name", "username").distinct()
    paginator = Paginator(patients, 20)
    page_number: str | None = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "avelon_healthcare/accounts/support_patient_list.html",
        {"page_obj": page_obj},
    )


@login_required
@support_required
def support_patient_update_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    Редагує особисті дані пацієнта для support.

    Args:
        request (HttpRequest): HTTP-запит.
        user_id (int): Ідентифікатор користувача.

    Returns:
        HttpResponse: HTML-відповідь або редірект.
    """
    patient: User = get_object_or_404(
        User.objects.filter(groups__name=PATIENT_GROUP_NAME).distinct(),
        id=user_id,
    )

    if request.method == "POST":
        form = SupportPatientUpdateForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            messages.success(request, "Дані пацієнта успішно оновлено.")
            return redirect("accounts:support_patient_list")
    else:
        form = SupportPatientUpdateForm(instance=patient)

    return render(
        request,
        "avelon_healthcare/accounts/support_patient_update.html",
        {
            "form": form,
            "patient": patient,
        },
    )

@login_required
def resend_verification_email_view(request: HttpRequest) -> HttpResponse:
    """
    Повторна відправка листа підтвердження email.
    Працює тільки якщо є pending_email.
    """

    user = request.user

    if not user.pending_email:
        messages.info(request, "Немає електронної пошти, що потребує підтвердження.")
        return redirect("accounts:profile")

    current_site = get_current_site(request)
    uid: str = urlsafe_base64_encode(force_bytes(user.pk))
    token: str = email_verification_token.make_token(user)

    verify_url: str = request.build_absolute_uri(
        reverse_lazy(
            "accounts:verify_email",
            kwargs={"uidb64": uid, "token": token},
        )
    )

    html_body: str = render_to_string(
        "avelon_healthcare/accounts/email_verification_email.html",
        {
            "user": user,
            "verify_url": verify_url,
            "domain": current_site.domain,
        },
    )

    send_html_email(
        subject="Avelon Healthcare — підтвердження електронної пошти",
        html_body=html_body,
        to=[user.pending_email],
    )

    messages.success(request, "Лист підтвердження повторно надіслано.")

    return redirect("accounts:profile")
