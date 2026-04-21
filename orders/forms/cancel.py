from __future__ import annotations

from django import forms


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