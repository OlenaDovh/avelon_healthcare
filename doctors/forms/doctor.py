"""Модуль `doctors/forms/doctor.py` застосунку `doctors`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations
from typing import Any

from django import forms
from django.contrib.auth import get_user_model

from accounts.constants import DOCTOR_GROUP
from doctors.models import Doctor

User = get_user_model()


class DoctorForm(forms.ModelForm):
    """Клас `DoctorForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.ModelForm`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    class Meta:
        """Клас `Meta` інкапсулює повʼязану логіку проєкту.

        Базові класи: `object`.
        Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
        """
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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Ініціалізує обʼєкт і встановлює початковий стан.

        Параметри:
            *args: Значення типу `Any`, яке передається для виконання логіки функції.
            **kwargs: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            None: Функція виконує дію без явного значення результату.
        """
        super().__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.filter(
            groups__name=DOCTOR_GROUP,
        ).distinct().order_by("last_name", "first_name", "username")

        self.fields["user"].label_from_instance = lambda obj: obj.full_name or obj.username
