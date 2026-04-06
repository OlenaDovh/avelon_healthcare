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

    Містить поля:
    - логін
    - email
    - телефон
    - пароль
    - підтвердження пароля
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
        """
        Метадані форми реєстрації.
        """

        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму реєстрації та налаштовує поля.

        Args:
            *args (Any): Позиційні аргументи.
            **kwargs (Any): Іменовані аргументи.

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
        Перевіряє унікальність email.

        Returns:
            str: Валідоване значення email.

        Raises:
            ValidationError: Якщо користувач із таким email вже існує.
        """
        email: str = self.cleaned_data["email"].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Користувач із такою електронною поштою вже існує.")

        return email


class LoginForm(forms.Form):
    """
    Форма входу користувача в систему.

    Дозволяє виконувати вхід за логіном або email.
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
        """
        Перевіряє коректність введених даних для авторизації.

        Returns:
            dict[str, Any]: Очищені дані форми.

        Raises:
            ValidationError: Якщо логін або пароль неправильні.
        """
        cleaned_data: dict[str, Any] = super().clean()
        login_value: str | None = cleaned_data.get("login")
        password: str | None = cleaned_data.get("password")

        user = authenticate(username=login_value, password=password)

        if user is None:
            raise ValidationError("Невірний логін/email або пароль.")

        cleaned_data["user"] = user
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма редагування профілю користувача.

    Дозволяє змінювати email, дату народження
    та пріоритетний канал зв'язку.
    Логін не редагується, телефон лише відображається окремо.
    """

    class Meta:
        """
        Метадані форми редагування профілю.
        """

        model = User
        fields = ("email", "birth_date", "preferred_contact_channel")
        widgets = {
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
        }
        labels = {
            "email": "Електронна пошта",
            "birth_date": "Дата народження",
            "preferred_contact_channel": "Пріоритетний канал зв'язку",
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму редагування профілю.

        Args:
            *args (Any): Позиційні аргументи.
            **kwargs (Any): Іменовані аргументи.

        Returns:
            None
        """
        super().__init__(*args, **kwargs)
        self.fields["preferred_contact_channel"].required = False
        self.fields["birth_date"].required = False

    def clean_email(self) -> str:
        """
        Перевіряє унікальність email під час редагування профілю.

        Returns:
            str: Валідований email.

        Raises:
            ValidationError: Якщо email уже використовується іншим користувачем.
        """
        email: str = self.cleaned_data["email"].lower()

        existing_user = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if existing_user.exists():
            raise ValidationError("Користувач із такою електронною поштою вже існує.")

        return email

from django.contrib.auth.forms import PasswordChangeForm


class UserPasswordChangeForm(PasswordChangeForm):
    """
    Форма зміни пароля для авторизованого користувача.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму зміни пароля та налаштовує поля.

        Args:
            *args (Any): Позиційні аргументи.
            **kwargs (Any): Іменовані аргументи.

        Returns:
            None
        """
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

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class UserPasswordResetForm(PasswordResetForm):
    """
    Форма запиту на відновлення пароля через email.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму запиту відновлення пароля.

        Args:
            *args (Any): Позиційні аргументи.
            **kwargs (Any): Іменовані аргументи.

        Returns:
            None
        """
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
        """
        Ініціалізує форму встановлення нового пароля.

        Args:
            *args (Any): Позиційні аргументи.
            **kwargs (Any): Іменовані аргументи.

        Returns:
            None
        """
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

