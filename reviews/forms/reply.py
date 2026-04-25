"""Модуль reviews/forms/reply.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django import forms
from reviews.models import Review

class ReviewReplyForm(forms.ModelForm):
    """Клас ReviewReplyForm.

Відповідає за поведінку, описану в цьому компоненті застосунку."""

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        model = Review
        fields = ('clinic_reply',)
        widgets = {'clinic_reply': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Введіть відповідь на відгук'})}
        labels = {'clinic_reply': 'Відповідь клініки'}
