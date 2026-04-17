from __future__ import annotations

from django import forms
from typing import Any

from accounts.selectors import patient_users_queryset
from analysis.models import Analysis
from .models import Order, OrderStatus, PaymentMethod


class GuestOrderForm(forms.Form):

    last_name = forms.CharField(
        label="Прізвище",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="Ім'я",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    middle_name = forms.CharField(
        label="По батькові",
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    phone = forms.CharField(
        label="Телефон",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    payment_method = forms.ChoiceField(
        label="Спосіб оплати",
        choices=PaymentMethod.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class AuthenticatedOrderForm(forms.Form):

    payment_method = forms.ChoiceField(
        label="Спосіб оплати",
        choices=PaymentMethod.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class OrderCancelForm(forms.Form):

    reason = forms.CharField(
        required=True,
        label="Причина скасування",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Вкажіть причину скасування",
            }
        ),
    )


class SupportOrderCreateForm(forms.Form):

    user = forms.ModelChoiceField(
        queryset=patient_users_queryset().order_by("last_name", "first_name").distinct(),
        required=False,
        label="Зареєстрований користувач",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    last_name = forms.CharField(
        required=False,
        label="Прізвище",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        required=False,
        label="Ім'я",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    middle_name = forms.CharField(
        required=False,
        label="По батькові",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    phone = forms.CharField(
        required=False,
        label="Телефон",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    payment_method = forms.ChoiceField(
        label="Спосіб оплати",
        choices=PaymentMethod.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    analyses = forms.ModelMultipleChoiceField(
        queryset=Analysis.objects.filter(is_active=True).order_by("name"),
        required=True,
        label="Аналізи",
        widget=forms.CheckboxSelectMultiple,
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        user = cleaned_data.get("user")

        last_name = cleaned_data.get("last_name")
        first_name = cleaned_data.get("first_name")
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")

        if not user and not all([last_name, first_name, phone, email]):
            raise forms.ValidationError(
                "Оберіть користувача або заповніть всі дані нового пацієнта."
            )

        return cleaned_data


class SupportOrderUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            "status",
            "rejection_reason",
            "payment_method",
            "result_file",
        )
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "rejection_reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "result_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }