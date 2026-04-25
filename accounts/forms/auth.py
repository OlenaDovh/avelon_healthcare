"""Модуль `accounts/forms/auth.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from typing import Any

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Форма для реєстрації нового користувача."""

    email = forms.EmailField(
        label="Електронна пошта",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@email.com",
            }
        ),
    )
    phone = forms.CharField(
        label="Номер телефону",
        help_text="Формат: +380XXXXXXXXX",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "+380XXXXXXXXX",
            }
        ),
    )

    class Meta:
        """Клас `Meta` інкапсулює повʼязану логіку проєкту.

        Базові класи: `object`.
        Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
        """
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "password1",
            "password2",
        )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму та налаштовує поля.

        Args:
            *args: Позиційні аргументи.
            **kwargs: Іменовані аргументи.

        Returns:
            None
        """
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Логін"
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введіть логін",
            }
        )

        self.fields["first_name"].label = "Ім'я"
        self.fields["first_name"].widget.attrs.update({"class": "form-control"})

        self.fields["last_name"].label = "Прізвище"
        self.fields["last_name"].widget.attrs.update({"class": "form-control"})

        self.fields["middle_name"].label = "По батькові"
        self.fields["middle_name"].required = False
        self.fields["middle_name"].widget.attrs.update({"class": "form-control"})

        self.fields["password1"].label = "Пароль"
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введіть пароль",
            }
        )

        self.fields["password2"].label = "Підтвердження пароля"
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторіть пароль",
            }
        )

    def clean_email(self) -> str:
        """
        Перевіряє унікальність email та нормалізує його.

        Returns:
            str: Валідований email.

        Raises:
            ValidationError: Якщо email вже існує або очікує підтвердження.
        """
        email: str = self.cleaned_data["email"].lower().strip()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Користувач із такою електронною поштою вже існує.")

        if User.objects.filter(pending_email__iexact=email).exists():
            raise ValidationError(
                "Ця електронна пошта вже очікує підтвердження в іншого користувача."
            )

        return email

    def clean_phone(self) -> str:
        """
        Перевіряє унікальність номера телефону.

        Returns:
            str: Валідований номер телефону.

        Raises:
            ValidationError: Якщо номер вже використовується.
        """
        phone: str = self.cleaned_data["phone"].strip()

        if User.objects.filter(phone=phone).exists():
            raise ValidationError("Користувач із таким номером телефону вже існує.")

        return phone


class LoginForm(forms.Form):
    """Форма для входу користувача."""

    login = forms.CharField(
        label="Логін або Email",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть логін або email",
            }
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть пароль",
            }
        ),
    )

    def clean(self) -> dict[str, Any]:
        """
        Аутентифікує користувача та додає його в cleaned_data.

        Returns:
            dict[str, Any]: Очищені дані форми з ключем 'user'.

        Raises:
            ValidationError: Якщо дані невірні або email не підтверджений.
        """
        cleaned_data: dict[str, Any] = super().clean()
        login_value: str | None = cleaned_data.get("login")
        password: str | None = cleaned_data.get("password")

        user = authenticate(username=login_value, password=password)

        if user is None:
            raise ValidationError("Невірний логін/email або пароль.")

        if not user.email_verified and not user.pending_email:
            raise ValidationError("Підтвердіть електронну пошту перед входом.")

        cleaned_data["user"] = user
        return cleaned_data
