"""Модуль `accounts/forms/passwords.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

from accounts.tasks import send_password_reset_email_task

from django.template.loader import render_to_string


class UserPasswordChangeForm(PasswordChangeForm):
    """Клас `UserPasswordChangeForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `PasswordChangeForm`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Ініціалізує обʼєкт і встановлює початковий стан.

        Параметри:
            *args: Значення типу `Any`, яке передається для виконання логіки функції.
            **kwargs: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            None: Функція виконує дію без явного значення результату.
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


class UserPasswordResetForm(PasswordResetForm):
    """Клас `UserPasswordResetForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `PasswordResetForm`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Ініціалізує обʼєкт і встановлює початковий стан.

        Параметри:
            *args: Значення типу `Any`, яке передається для виконання логіки функції.
            **kwargs: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            None: Функція виконує дію без явного значення результату.
        """
        super().__init__(*args, **kwargs)

        self.fields["email"].label = "Електронна пошта"
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введіть вашу електронну пошту",
            }
        )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):

        """Виконує прикладну логіку функції `send_mail` у відповідному модулі проєкту.

        Параметри:
            subject_template_name: Значення типу `Any`, яке передається для виконання логіки функції.
            email_template_name: Значення типу `Any`, яке передається для виконання логіки функції.
            context: Значення типу `Any`, яке передається для виконання логіки функції.
            from_email: Значення типу `Any`, яке передається для виконання логіки функції.
            to_email: Значення типу `Any`, яке передається для виконання логіки функції.
            html_email_template_name: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            None: Функція виконує дію без явного значення результату.
        """
        subject = render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())

        body = render_to_string(email_template_name, context)

        html_email = None
        if html_email_template_name:
            html_email = render_to_string(html_email_template_name, context)

        send_password_reset_email_task.delay(
            subject=subject,
            body=body,
            from_email=from_email,
            to_email=to_email,
            html_email=html_email,
        )


class UserSetPasswordForm(SetPasswordForm):
    """Клас `UserSetPasswordForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `SetPasswordForm`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Ініціалізує обʼєкт і встановлює початковий стан.

        Параметри:
            *args: Значення типу `Any`, яке передається для виконання логіки функції.
            **kwargs: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            None: Функція виконує дію без явного значення результату.
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
