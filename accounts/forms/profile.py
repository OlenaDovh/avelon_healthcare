from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма для редагування профілю користувача.

    Дозволяє оновлювати персональні дані з перевіркою унікальності email і телефону.
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
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
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
        """
        Ініціалізує форму та налаштовує необов'язкові поля.

        Args:
            *args: Позиційні аргументи.
            **kwargs: Іменовані аргументи.
        """
        super().__init__(*args, **kwargs)

        self.fields["preferred_contact_channel"].required = False
        self.fields["birth_date"].required = False
        self.fields["middle_name"].required = False

    def clean_email(self) -> str:
        """
        Перевіряє унікальність email та нормалізує його.

        Returns:
            str: Валідований email у нижньому регістрі.

        Raises:
            ValidationError: Якщо email вже використовується або очікує підтвердження.
        """
        email = self.cleaned_data["email"].lower().strip()

        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Користувач із такою електронною поштою вже існує.")

        if User.objects.filter(pending_email__iexact=email).exclude(pk=self.instance.pk).exists():
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
        phone = self.cleaned_data["phone"].strip()

        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Користувач із таким номером телефону вже існує.")

        return phone
