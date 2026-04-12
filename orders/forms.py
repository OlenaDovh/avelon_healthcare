from __future__ import annotations

from django import forms

from .models import PaymentMethod


class GuestOrderForm(forms.Form):
    """
    Форма для оформлення замовлення неавторизованим користувачем.
    """

    full_name: forms.CharField = forms.CharField(
        label="ПІБ",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть ПІБ",
            }
        ),
    )
    phone: forms.CharField = forms.CharField(
        label="Телефон",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть телефон",
            }
        ),
    )
    email: forms.EmailField = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть email",
            }
        ),
    )
    payment_method: forms.ChoiceField = forms.ChoiceField(
        label="Спосіб оплати",
        choices=PaymentMethod.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )


class AuthenticatedOrderForm(forms.Form):
    """
    Форма для оформлення замовлення авторизованим користувачем.
    """

    payment_method: forms.ChoiceField = forms.ChoiceField(
        label="Спосіб оплати",
        choices=PaymentMethod.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )