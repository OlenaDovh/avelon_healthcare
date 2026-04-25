from __future__ import annotations
from django import forms
from reviews.models import Review


class ReviewReplyForm(forms.ModelForm):
    """
    Форма відповіді клініки на відгук.
    """

    class Meta:
        model = Review
        fields = ("clinic_reply",)
        widgets = {
            "clinic_reply": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Введіть відповідь на відгук",
                }
            ),
        }
        labels = {
            "clinic_reply": "Відповідь клініки",
        }

    def clean_clinic_reply(self) -> str:
        """
        Очищає та валідовує відповідь клініки.

        Returns:
            str: Очищений текст відповіді.
        """
        text: str = self.cleaned_data["clinic_reply"].strip()

        if not text:
            raise forms.ValidationError("Відповідь не може бути порожньою.")

        return text
