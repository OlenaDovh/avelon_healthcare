"""Модуль `accounts/forms/support.py` застосунку `accounts`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations
from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class SupportPatientUpdateForm(forms.ModelForm):
    """
    Форма редагування пацієнта для support.
    """

    class Meta:
        """Клас `Meta` інкапсулює повʼязану логіку проєкту.

        Базові класи: `object`.
        Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
        """
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
        """Ініціалізує обʼєкт і встановлює початковий стан.

        Параметри:
            *args: Значення типу `Any`, яке передається для виконання логіки функції.
            **kwargs: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            None: Функція виконує дію без явного значення результату.
        """
        super().__init__(*args, **kwargs)
        self.fields["middle_name"].required = False
        self.fields["birth_date"].required = False
        self.fields["preferred_contact_channel"].required = False

    def clean_phone(self) -> str:
        """Виконує прикладну логіку функції `clean_phone` у відповідному модулі проєкту.

        Повертає:
            str: Результат роботи функції або обʼєкт, сформований під час виконання.
        """
        phone: str = self.cleaned_data["phone"].strip()

        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Користувач із таким номером телефону вже існує.")

        return phone

    def clean_discount(self) -> int:
        """Виконує прикладну логіку функції `clean_discount` у відповідному модулі проєкту.

        Повертає:
            int: Результат роботи функції або обʼєкт, сформований під час виконання.
        """
        discount: int = self.cleaned_data["discount"]

        if discount < 0 or discount > 100:
            raise ValidationError("Знижка має бути від 0 до 100%.")

        return discount
