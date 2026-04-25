from __future__ import annotations
from django import forms
from support_chat.models import SupportChatTopic

class SupportChatGuestStartForm(forms.Form):
    """Описує клас `SupportChatGuestStartForm`."""
    guest_name = forms.CharField(label="Ваше ім'я", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    guest_email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    topic = forms.ChoiceField(label='Тема звернення', choices=SupportChatTopic.choices, widget=forms.Select(attrs={'class': 'form-select'}))
    initial_description = forms.CharField(label='Опишіть ваше питання', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

class SupportChatUserStartForm(forms.Form):
    """Описує клас `SupportChatUserStartForm`."""
    topic = forms.ChoiceField(label='Тема звернення', choices=SupportChatTopic.choices, widget=forms.Select(attrs={'class': 'form-select'}))
    initial_description = forms.CharField(label='Опишіть ваше питання', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
