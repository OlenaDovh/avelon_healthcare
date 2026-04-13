from __future__ import annotations

from datetime import datetime
from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Count

from doctors.models import Direction, Doctor

from .models import Appointment
from .utils import get_available_slots_for_doctor_on_date


class AppointmentCreateForm(forms.ModelForm):
    """
    Базова форма створення запису до лікаря.
    """

    appointment_time = forms.ChoiceField(
        required=True,
        label="Час прийому",
        widget=forms.Select(attrs={"class": "form-select"}),
        choices=[("", "Оберіть час")],
    )

    class Meta:
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
            "appointment_date": forms.TextInput(
                attrs={"class": "form-control", "autocomplete": "off"}
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
            "description": "Опис",
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Ініціалізує форму.

        Returns:
            None
        """
        super().__init__(*args, **kwargs)

        self.fields["direction"].queryset = Direction.objects.annotate(
            doctors_count=Count("doctors")
        ).filter(doctors_count__gt=0).order_by("name")
        self.fields["doctor"].queryset = Doctor.objects.none()
        self.fields["appointment_time"].choices = [("", "Оберіть час")]

        direction_id = self.data.get("direction") or self.initial.get("direction")
        doctor_id = self.data.get("doctor") or self.initial.get("doctor")
        appointment_date = self.data.get("appointment_date") or self.initial.get("appointment_date")

        if direction_id:
            self.fields["doctor"].queryset = Doctor.objects.filter(
                directions__id=direction_id
            ).distinct().order_by("full_name")

        if direction_id and doctor_id and appointment_date:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                direction = Direction.objects.get(id=direction_id)
                target_date = forms.DateField().clean(appointment_date)
                slots = get_available_slots_for_doctor_on_date(doctor, direction, target_date)
                self.fields["appointment_time"].choices = [
                    ("", "Оберіть час"),
                    *[(slot["value"], slot["label"]) for slot in slots],
                ]
            except (Doctor.DoesNotExist, Direction.DoesNotExist, ValidationError):
                pass

    def clean(self) -> dict[str, Any]:
        """
        Виконує загальну валідацію форми.

        Returns:
            dict[str, Any]: Очищені дані форми.
        """
        cleaned_data = super().clean()

        direction = cleaned_data.get("direction")
        doctor = cleaned_data.get("doctor")
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        if direction and doctor and not doctor.directions.filter(id=direction.id).exists():
            raise ValidationError("Обраний лікар не працює в цьому напрямі.")

        if doctor and direction and appointment_date and appointment_time:
            slots = get_available_slots_for_doctor_on_date(doctor, direction, appointment_date)
            available_values = {slot["value"] for slot in slots}

            if appointment_time not in available_values:
                raise ValidationError("Цей часовий слот уже недоступний.")

            cleaned_data["appointment_time"] = datetime.strptime(
                appointment_time,
                "%H:%M",
            ).time()

        return cleaned_data


class GuestAppointmentCreateForm(AppointmentCreateForm):
    """
    Форма створення запису для неавторизованого користувача.
    """

    full_name = forms.CharField(
        label="ПІБ",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть ПІБ",
            }
        ),
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть телефон",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть email",
            }
        ),
    )

    class Meta(AppointmentCreateForm.Meta):
        fields = (
            "full_name",
            "phone",
            "email",
            "direction",
            "doctor",
            "appointment_date",
            "appointment_time",
            "description",
        )