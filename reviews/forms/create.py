from __future__ import annotations
from django import forms
from reviews.models import Review

class ReviewCreateForm(forms.ModelForm):
    """Описує клас `ReviewCreateForm`."""

    class Meta:
        """Описує клас `Meta`."""
        model = Review
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Напишіть ваш відгук про прийом'})}
        labels = {'text': 'Текст відгуку'}

    def clean_text(self) -> str:
        """Виконує логіку `clean_text`.

Returns:
    Any: Результат виконання."""
        text: str = self.cleaned_data['text'].strip()
        return text
