"""Модуль `reviews/forms/reply.py` застосунку `reviews`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django import forms

from reviews.models import Review


class ReviewReplyForm(forms.ModelForm):
    """Клас `ReviewReplyForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.ModelForm`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    class Meta:
        """Клас `Meta` інкапсулює повʼязану логіку проєкту.

        Базові класи: `object`.
        Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
        """
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
