from __future__ import annotations

from typing import Any

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterForm(UserCreationForm):
    """
    Форма реєстрації нового користувача.
    """

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
        email: str = self.cleaned_data["email"].lower().strip()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Користувач із такою електронною поштою вже існує.")

        if User.objects.filter(pending_email__iexact=email).exists():
            raise ValidationError(
                "Ця електронна пошта вже очікує підтвердження в іншого користувача."
            )

        return email

    def clean_phone(self) -> str:
        phone: str = self.cleaned_data["phone"].strip()

        if User.objects.filter(phone=phone).exists():
            raise ValidationError("Користувач із таким номером телефону вже існує.")

        return phone


class LoginForm(forms.Form):
    """
    Форма входу користувача.
    """

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