from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class SupportPatientUpdateForm(forms.ModelForm):
    """
    Форма редагування пацієнта для support.

    Дозволяє оновлювати персональні дані та знижку з валідацією значень.
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
                    "max": 100,
                }
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму та налаштовує необов'язкові поля.

        Args:
            *args: Позиційні аргументи.
            **kwargs: Іменовані аргументи.
        """
        super().__init__(*args, **kwargs)
        self.fields["middle_name"].required = False
        self.fields["birth_date"].required = False
        self.fields["preferred_contact_channel"].required = False

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

    def clean_discount(self) -> int:
        """
        Перевіряє коректність значення знижки.

        Returns:
            int: Валідоване значення знижки.

        Raises:
            ValidationError: Якщо значення виходить за межі 0–100.
        """
        discount = self.cleaned_data["discount"]

        if discount < 0 or discount > 100:
            raise ValidationError("Знижка має бути від 0 до 100%.")

        return discount
