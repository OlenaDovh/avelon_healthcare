"""Модуль orders/forms/cancel.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django import forms

class OrderCancelForm(forms.Form):
    """Клас OrderCancelForm.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    reason = forms.CharField(required=True, label='Причина скасування', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Вкажіть причину скасування'}))
