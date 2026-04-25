"""Модуль `support_chat/forms/start.py` застосунку `support_chat`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django import forms

from support_chat.models import SupportChatTopic


class SupportChatGuestStartForm(forms.Form):
    """Клас `SupportChatGuestStartForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.Form`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
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


class SupportChatUserStartForm(forms.Form):
    """Клас `SupportChatUserStartForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.Form`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
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
