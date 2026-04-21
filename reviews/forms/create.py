from __future__ import annotations

from django import forms

from reviews.models import Review


class ReviewCreateForm(forms.ModelForm):
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
        text: str = self.cleaned_data["text"].strip()
        return text