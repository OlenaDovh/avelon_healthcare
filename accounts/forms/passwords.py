from typing import Any
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.template.loader import render_to_string
from accounts.tasks import send_password_reset_email_task


class UserPasswordChangeForm(PasswordChangeForm):
    """
    Форма для зміни пароля користувача.

    Налаштовує відображення полів та їх атрибути.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму та налаштовує поля.

        Args:
            *args: Позиційні аргументи.
            **kwargs: Іменовані аргументи.
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
    """
    Форма для відновлення пароля користувача.

    Відправляє email з інструкціями для скидання пароля.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму та налаштовує поле email.

        Args:
            *args: Позиційні аргументи.
            **kwargs: Іменовані аргументи.
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
            subject_template_name: str,
            email_template_name: str,
            context: dict[str, Any],
            from_email: str,
            to_email: str,
            html_email_template_name: str | None = None,
    ) -> None:
        """
        Формує та надсилає лист для скидання пароля.

        Args:
            subject_template_name: Шаблон теми листа.
            email_template_name: Шаблон текстового листа.
            context: Контекст для рендерингу шаблонів.
            from_email: Email відправника.
            to_email: Email отримувача.
            html_email_template_name: Шаблон HTML-листа.

        Returns:
            None
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
    """
    Форма для встановлення нового пароля користувача.

    Використовується після підтвердження скидання пароля.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму та налаштовує поля.

        Args:
            *args: Позиційні аргументи.
            **kwargs: Іменовані аргументи.
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
