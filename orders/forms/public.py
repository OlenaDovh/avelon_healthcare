from __future__ import annotations
from django import forms
from orders.models import PaymentMethod


class GuestOrderForm(forms.Form):
    """
    Форма оформлення замовлення для незареєстрованого користувача.

    Збирає персональні дані та спосіб оплати.
    """

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
    """
    Форма оформлення замовлення для авторизованого користувача.

    Дозволяє обрати лише спосіб оплати.
    """

    payment_method = forms.ChoiceField(
        label="Спосіб оплати",
        choices=PaymentMethod.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )