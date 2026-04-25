from __future__ import annotations
from typing import Any
from django import forms
from accounts.selectors import patient_users_queryset
from analysis.models import Analysis
from orders.models import Order, PaymentMethod


class SupportOrderCreateForm(forms.Form):
    """
    Форма створення замовлення співробітником support.

    Дозволяє обрати зареєстрованого користувача або ввести дані нового пацієнта,
    а також вибрати аналізи та спосіб оплати.
    """

    user = forms.ModelChoiceField(
        queryset=patient_users_queryset().order_by("last_name", "first_name").distinct(),
        required=False,
        label="Зареєстрований користувач",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    last_name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(required=False, max_length=150,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    middle_name = forms.CharField(required=False, max_length=150,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))

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
        """
        Виконує валідацію форми.

        Перевіряє, що або обрано користувача, або заповнені всі обов'язкові поля гостя.

        Returns:
            dict[str, Any]: Очищені дані форми.

        Raises:
            ValidationError: Якщо не заповнено необхідні дані.
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
    """
    Форма оновлення замовлення співробітником support.

    Дозволяє змінювати статус, причину відхилення, спосіб оплати та файл результату.
    """

    class Meta:
        model = Order
        fields = ("status", "rejection_reason", "payment_method", "result_file")
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "rejection_reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "result_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
