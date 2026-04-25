from __future__ import annotations
from django import forms
from django.contrib.auth import get_user_model
from accounts.constants import DOCTOR_GROUP
from doctors.models import Doctor

User = get_user_model()


class DoctorForm(forms.ModelForm):
    """
    Форма для створення та редагування лікаря.

    Використовується для керування об'єктами моделі Doctor.
    """

    class Meta:
        model = Doctor
        fields = (
            "user",
            "last_name",
            "first_name",
            "middle_name",
            "position",
            "directions",
            "qualification_category",
            "experience_years",
            "price_from",
            "price_to",
            "photo",
            "work_experience_description",
            "when_to_contact",
            "education",
            "licenses",
        )
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "directions": forms.CheckboxSelectMultiple(),
            "qualification_category": forms.TextInput(attrs={"class": "form-control"}),
            "experience_years": forms.NumberInput(attrs={"class": "form-control"}),
            "price_from": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "price_to": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "work_experience_description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "when_to_contact": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "education": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "licenses": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs) -> None:
        """
        Ініціалізує форму та налаштовує queryset для користувачів.

        Args:
            *args: Позиційні аргументи.
            **kwargs: Іменовані аргументи.

        Returns:
            None
        """
        super().__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.filter(
            groups__name=DOCTOR_GROUP,
        ).distinct().order_by("last_name", "first_name", "username")

        self.fields["user"].label_from_instance = lambda obj: obj.full_name or obj.username
