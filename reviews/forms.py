from __future__ import annotations

from typing import Any

from django import forms

from .models import Review


class ReviewCreateForm(forms.ModelForm):
    """
    Форма створення відгуку.
    """

    class Meta:
        """
        Метадані форми створення відгуку.
        """

        model = Review
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Напишіть ваш відгук про прийом",
                }
            ),
        }
        labels = {
            "text": "Текст відгуку",
        }

    def clean_text(self) -> str:
        """
        Перевіряє, що текст не порожній.

        Returns:
            str: Очищений текст відгуку.
        """
        text: str = self.cleaned_data["text"].strip()
        return text