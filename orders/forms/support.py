"""Модуль `orders/forms/support.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from typing import Any

from django import forms

from accounts.selectors import patient_users_queryset
from analysis.models import Analysis
from orders.models import Order, PaymentMethod


class SupportOrderCreateForm(forms.Form):
    """Клас `SupportOrderCreateForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.Form`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    user = forms.ModelChoiceField(
        queryset=patient_users_queryset().order_by("last_name", "first_name").distinct(),
        required=False,
        label="Зареєстрований користувач",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    last_name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    middle_name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))

    phone = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control"}))

    payment_method = forms.ChoiceField(
        choices=PaymentMethod.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    analyses = forms.ModelMultipleChoiceField(
        queryset=Analysis.objects.filter(is_active=True).order_by("name"),
        widget=forms.CheckboxSelectMultiple,
    )

    def clean(self) -> dict[str, Any]:
        """Перевіряє, очищує та нормалізує введені дані.

        Повертає:
            dict[str, Any]: Результат роботи функції або обʼєкт, сформований під час виконання.
        """
        cleaned_data = super().clean()

        user = cleaned_data.get("user")

        if not user:
            required = [
                cleaned_data.get("last_name"),
                cleaned_data.get("first_name"),
                cleaned_data.get("phone"),
                cleaned_data.get("email"),
            ]
            if not all(required):
                raise forms.ValidationError(
                    "Оберіть користувача або заповніть всі дані нового пацієнта."
                )

        return cleaned_data


class SupportOrderUpdateForm(forms.ModelForm):
    """Клас `SupportOrderUpdateForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.ModelForm`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    class Meta:
        """Клас `Meta` інкапсулює повʼязану логіку проєкту.

        Базові класи: `object`.
        Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
        """
        model = Order
        fields = ("status", "rejection_reason", "payment_method", "result_file")
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "rejection_reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "result_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
