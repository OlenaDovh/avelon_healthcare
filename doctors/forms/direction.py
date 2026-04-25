"""Модуль doctors/forms/direction.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django import forms
from doctors.models import Direction

class DirectionForm(forms.ModelForm):
    """Клас DirectionForm.

Відповідає за поведінку, описану в цьому компоненті застосунку."""

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        model = Direction
        fields = ('name', 'description')
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}), 'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})}
