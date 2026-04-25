"""Модуль reviews/forms/create.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django import forms
from reviews.models import Review

class ReviewCreateForm(forms.ModelForm):
    """Клас ReviewCreateForm.

Відповідає за поведінку, описану в цьому компоненті застосунку."""

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        model = Review
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Напишіть ваш відгук про прийом'})}
        labels = {'text': 'Текст відгуку'}

    def clean_text(self) -> str:
        """Виконує логіку `clean_text`.

Returns:
    Результат виконання операції."""
        text: str = self.cleaned_data['text'].strip()
        return text
