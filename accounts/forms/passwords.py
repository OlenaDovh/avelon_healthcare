from __future__ import annotations
from typing import Any
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from accounts.tasks import send_password_reset_email_task
from django.template.loader import render_to_string

class UserPasswordChangeForm(PasswordChangeForm):
    """Описує клас `UserPasswordChangeForm`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Виконує логіку `__init__`.

Args:
    *args: Вхідний параметр `args`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Поточний пароль'
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введіть поточний пароль'})
        self.fields['new_password1'].label = 'Новий пароль'
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введіть новий пароль'})
        self.fields['new_password2'].label = 'Підтвердження нового пароля'
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторіть новий пароль'})

class UserPasswordResetForm(PasswordResetForm):
    """Описує клас `UserPasswordResetForm`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Виконує логіку `__init__`.

Args:
    *args: Вхідний параметр `args`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Електронна пошта'
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введіть вашу електронну пошту'})

    def send_mail(self, subject_template_name: Any, email_template_name: Any, context: Any, from_email: Any, to_email: Any, html_email_template_name: Any=None) -> None:
        """Виконує логіку `send_mail`.

Args:
    subject_template_name: Вхідний параметр `subject_template_name`.
    email_template_name: Вхідний параметр `email_template_name`.
    context: Вхідний параметр `context`.
    from_email: Вхідний параметр `from_email`.
    to_email: Вхідний параметр `to_email`.
    html_email_template_name: Вхідний параметр `html_email_template_name`.

Returns:
    Any: Результат виконання."""
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)
        html_email = None
        if html_email_template_name:
            html_email = render_to_string(html_email_template_name, context)
        send_password_reset_email_task.delay(subject=subject, body=body, from_email=from_email, to_email=to_email, html_email=html_email)

class UserSetPasswordForm(SetPasswordForm):
    """Описує клас `UserSetPasswordForm`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Виконує логіку `__init__`.

Args:
    *args: Вхідний параметр `args`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Новий пароль'
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введіть новий пароль'})
        self.fields['new_password2'].label = 'Підтвердження нового пароля'
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторіть новий пароль'})
