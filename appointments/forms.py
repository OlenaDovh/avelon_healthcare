from __future__ import annotations

from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from doctors.models import Direction, Doctor

from .models import Appointment


class AppointmentCreateForm(forms.ModelForm):
    """
    Форма створення запису до лікаря.
    """

    class Meta:
        """
        Метадані форми запису.
        """

        model = Appointment
        fields = (
            "direction",
            "doctor",
            "appointment_date",
            "appointment_time",
            "description",
        )
        widgets = {
            "direction": forms.Select(attrs={"class": "form-select"}),
            "doctor": forms.Select(attrs={"class": "form-select"}),
            "appointment_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "appointment_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Опишіть причину звернення до лікаря",
                }
            ),
        }
        labels = {
            "direction": "Напрям",
            "doctor": "Лікар",
            "appointment_date": "Дата прийому",
            "appointment_time": "Час прийому",
            "description": "Опис",
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму запису до лікаря.

        Args:
            *args (Any): Позиційні аргументи.
            **kwargs (Any): Іменовані аргументи.

        Returns:
            None
        """
        super().__init__(*args, **kwargs)

        self.fields["direction"].queryset = Direction.objects.all()
        self.fields["doctor"].queryset = Doctor.objects.all()

    def clean(self) -> dict[str, Any]:
        """
        Перевіряє коректність введених даних.

        Returns:
            dict[str, Any]: Очищені дані форми.

        Raises:
            ValidationError: Якщо лікар не належить до напряму
            або слот уже зайнятий.
        """
        cleaned_data: dict[str, Any] = super().clean()

        direction = cleaned_data.get("direction")
        doctor = cleaned_data.get("doctor")
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        if direction and doctor:
            if not doctor.directions.filter(id=direction.id).exists():
                raise ValidationError("Обраний лікар не працює в цьому напрямі.")

        if doctor and appointment_date and appointment_time:
            exists = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            ).exists()
            if exists:
                raise ValidationError(
                    "Цей часовий слот уже зайнятий. Оберіть інший час."
                )

        return cleaned_data