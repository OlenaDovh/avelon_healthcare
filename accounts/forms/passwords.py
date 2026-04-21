from __future__ import annotations

from typing import Any

from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)


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