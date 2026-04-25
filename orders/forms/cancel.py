from __future__ import annotations
from django import forms


class OrderCancelForm(forms.Form):
    """
    Форма для скасування замовлення.

    Використовується для введення причини скасування.
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
