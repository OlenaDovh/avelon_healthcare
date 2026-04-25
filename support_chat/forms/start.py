from __future__ import annotations
from django import forms
from support_chat.models import SupportChatTopic


class SupportChatGuestStartForm(forms.Form):
    """
    Форма старту чату для незареєстрованого користувача.
    """

    guest_name = forms.CharField(
        label="Ваше ім'я",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    guest_email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    topic = forms.ChoiceField(
        label="Тема звернення",
        choices=SupportChatTopic.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    initial_description = forms.CharField(
        label="Опишіть ваше питання",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
    )

    def clean_initial_description(self) -> str:
        """
        Очищає текст повідомлення.
        """
        text = self.cleaned_data["initial_description"].strip()

        if not text:
            raise forms.ValidationError("Будь ласка, опишіть ваше питання.")

        return text


class SupportChatUserStartForm(forms.Form):
    """
    Форма старту чату для авторизованого користувача.
    """

    topic = forms.ChoiceField(
        label="Тема звернення",
        choices=SupportChatTopic.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    initial_description = forms.CharField(
        label="Опишіть ваше питання",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
    )

    def clean_initial_description(self) -> str:
        """
        Очищає текст повідомлення.
        """
        text = self.cleaned_data["initial_description"].strip()

        if not text:
            raise forms.ValidationError("Будь ласка, опишіть ваше питання.")

        return text
