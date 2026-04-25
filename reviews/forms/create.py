from __future__ import annotations
from django import forms
from reviews.models import Review


class ReviewCreateForm(forms.ModelForm):
    """
    Форма створення відгуку.

    Дозволяє користувачу залишити текстовий відгук про прийом.
    """

    class Meta:
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
        Очищає текст відгуку від зайвих пробілів.

        Returns:
            str: Очищений текст.
        """
        text: str = self.cleaned_data["text"].strip()

        if not text:
            raise forms.ValidationError("Текст відгуку не може бути порожнім.")

        return text
