from __future__ import annotations
from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()

class SupportPatientUpdateForm(forms.ModelForm):
    """
    Форма редагування пацієнта для support.
    """

    class Meta:
        """Описує клас `Meta`."""
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone', 'birth_date', 'preferred_contact_channel', 'discount')
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}), 'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}), 'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'По батькові'}), 'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380XXXXXXXXX'}), 'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 'preferred_contact_channel': forms.Select(attrs={'class': 'form-select'}), 'discount': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100})}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Виконує логіку `__init__`.

Args:
    *args: Вхідний параметр `args`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        super().__init__(*args, **kwargs)
        self.fields['middle_name'].required = False
        self.fields['birth_date'].required = False
        self.fields['preferred_contact_channel'].required = False

    def clean_phone(self) -> str:
        """Виконує логіку `clean_phone`.

Returns:
    Any: Результат виконання."""
        phone: str = self.cleaned_data['phone'].strip()
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Користувач із таким номером телефону вже існує.')
        return phone

    def clean_discount(self) -> int:
        """Виконує логіку `clean_discount`.

Returns:
    Any: Результат виконання."""
        discount: int = self.cleaned_data['discount']
        if discount < 0 or discount > 100:
            raise ValidationError('Знижка має бути від 0 до 100%.')
        return discount
