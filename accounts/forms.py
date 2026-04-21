from __future__ import annotations

from typing import Any

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
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
        self.fields["first_name"].widget.attrs.update(
            {"class": "form-control"}
        )

        self.fields["last_name"].label = "Прізвище"
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control"}
        )

        self.fields["middle_name"].label = "По батькові"
        self.fields["middle_name"].required = False
        self.fields["middle_name"].widget.attrs.update(
            {"class": "form-control"}
        )

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
            raise ValidationError("Ця електронна пошта вже очікує підтвердження в іншого користувача.")

        return email


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


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма редагування профілю користувача.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "birth_date",
            "preferred_contact_channel",
        )
        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+380XXXXXXXXX",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@email.com",
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "preferred_contact_channel": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }
        labels = {
            "email": "Електронна пошта",
            "birth_date": "Дата народження",
            "preferred_contact_channel": "Пріоритетний канал зв'язку",
            "phone": "Номер телефону",
            "first_name": "Ім'я",
            "last_name": "Прізвище",
            "middle_name": "По батькові",
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["preferred_contact_channel"].required = False
        self.fields["birth_date"].required = False
        self.fields["middle_name"].required = False

    def clean_email(self) -> str:
        email: str = self.cleaned_data["email"].lower().strip()

        existing_user = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if existing_user.exists():
            raise ValidationError("Користувач із такою електронною поштою вже існує.")

        existing_pending = User.objects.filter(pending_email__iexact=email).exclude(pk=self.instance.pk)
        if existing_pending.exists():
            raise ValidationError("Ця електронна пошта вже очікує підтвердження в іншого користувача.")

        return email

    def clean_phone(self) -> str:
        phone: str = self.cleaned_data["phone"].strip()

        existing_user = User.objects.filter(phone=phone).exclude(pk=self.instance.pk)
        if existing_user.exists():
            raise ValidationError("Користувач із таким номером телефону вже існує.")

        return phone


class UserPasswordChangeForm(PasswordChangeForm):
    """
    Форма зміни пароля для авторизованого користувача.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields["old_password"].label = "Поточний пароль"
        self.fields["old_password"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введіть поточний пароль",
            }
        )

        self.fields["new_password1"].label = "Новий пароль"
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введіть новий пароль",
            }
        )

        self.fields["new_password2"].label = "Підтвердження нового пароля"
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторіть новий пароль",
            }
        )


class UserPasswordResetForm(PasswordResetForm):
    """
    Форма запиту на відновлення пароля через email.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields["email"].label = "Електронна пошта"
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введіть вашу електронну пошту",
            }
        )


class UserSetPasswordForm(SetPasswordForm):
    """
    Форма встановлення нового пароля після переходу за посиланням із листа.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields["new_password1"].label = "Новий пароль"
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введіть новий пароль",
            }
        )

        self.fields["new_password2"].label = "Підтвердження нового пароля"
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторіть новий пароль",
            }
        )


class SupportPatientUpdateForm(forms.ModelForm):
    """
    Форма редагування пацієнта для support.
    """

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "phone",
            "birth_date",
            "preferred_contact_channel",
            "discount",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ім'я",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Прізвище",
                }
            ),
            "middle_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "По батькові",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+380XXXXXXXXX",
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "preferred_contact_channel": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "discount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
        }

    def clean_phone(self) -> str:
        phone: str = self.cleaned_data["phone"]

        existing_user = User.objects.filter(phone=phone).exclude(pk=self.instance.pk)
        if existing_user.exists():
            raise ValidationError("Користувач із таким номером телефону вже існує.")

        return phone