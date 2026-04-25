"""Модуль `doctors/forms/schedule.py` застосунку `doctors`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations
from typing import Any

from django import forms
from django.forms import inlineformset_factory

from doctors.models import Direction, Doctor, DoctorWorkDay, DoctorWorkPeriod


class DoctorWorkDayForm(forms.ModelForm):
    """Клас `DoctorWorkDayForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.ModelForm`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    class Meta:
        """Клас `Meta` інкапсулює повʼязану логіку проєкту.

        Базові класи: `object`.
        Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
        """
        model = DoctorWorkDay
        fields = (
            "doctor",
            "direction",
            "work_date",
            "appointment_duration_minutes",
        )
        widgets = {
            "doctor": forms.Select(attrs={"class": "form-select"}),
            "direction": forms.Select(attrs={"class": "form-select"}),
            "work_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "appointment_duration_minutes": forms.Select(attrs={"class": "form-select"}),
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

        self.fields["doctor"].queryset = Doctor.objects.prefetch_related("directions").order_by(
            "last_name",
            "first_name",
        )
        self.fields["direction"].queryset = Direction.objects.none()

        doctor_id = self.data.get("doctor") or getattr(self.instance, "doctor_id", None)

        if doctor_id:
            self.fields["direction"].queryset = Direction.objects.filter(
                doctors__id=doctor_id,
            ).distinct().order_by("name")
        elif self.instance.pk and self.instance.doctor_id:
            self.fields["direction"].queryset = self.instance.doctor.directions.all().order_by("name")


class DoctorWorkPeriodForm(forms.ModelForm):
    """Клас `DoctorWorkPeriodForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.ModelForm`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    class Meta:
        """Клас `Meta` інкапсулює повʼязану логіку проєкту.

        Базові класи: `object`.
        Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
        """
        model = DoctorWorkPeriod
        fields = ("start_time", "end_time")
        widgets = {
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
        }


DoctorWorkPeriodFormSet = inlineformset_factory(
    DoctorWorkDay,
    DoctorWorkPeriod,
    form=DoctorWorkPeriodForm,
    extra=1,
    can_delete=False,
)
