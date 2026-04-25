"""Модуль `orders/forms/cancel.py` застосунку `orders`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django import forms


class OrderCancelForm(forms.Form):
    """Клас `OrderCancelForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.Form`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
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
