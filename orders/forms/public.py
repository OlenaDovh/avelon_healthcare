"""Модуль `orders/forms/public.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django import forms

from orders.models import PaymentMethod


class GuestOrderForm(forms.Form):
    """Клас `GuestOrderForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.Form`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
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
    """Клас `AuthenticatedOrderForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.Form`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    payment_method = forms.ChoiceField(
        label="Спосіб оплати",
        choices=PaymentMethod.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
