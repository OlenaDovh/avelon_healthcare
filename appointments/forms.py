from __future__ import annotations

from datetime import datetime
from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils import timezone

from accounts.selectors import patient_users_queryset
from doctors.models import Direction, Doctor

from .models import Appointment, AppointmentStatus
from .utils import (
    get_available_dates_for_doctor_direction,
    get_available_slots_for_doctor_on_date,
)

class AppointmentCreateForm(forms.ModelForm):
    appointment_date = forms.DateField(
        required=True,
        label="Дата прийому",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Оберіть дату",
            }
        ),
    )

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
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Опишіть причину звернення до лікаря",
                }
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields["direction"].queryset = (
            Direction.objects.annotate(doctors_count=Count("doctors"))
            .filter(doctors_count__gt=0)
            .order_by("name")
        )

        self.fields["doctor"].queryset = Doctor.objects.none()
        self.fields["appointment_time"].choices = [("", "Оберіть час")]

        direction_id = self.data.get("direction") or self.initial.get("direction")
        doctor_id = self.data.get("doctor") or self.initial.get("doctor")
        appointment_date = self.data.get("appointment_date") or self.initial.get("appointment_date")

        if direction_id:
            self.fields["doctor"].queryset = (
                Doctor.objects.filter(directions__id=direction_id)
                .distinct()
                .order_by("last_name", "first_name")
            )

        if direction_id and doctor_id and appointment_date:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                direction = Direction.objects.get(id=direction_id)
                target_date = forms.DateField().clean(appointment_date)

                slots = get_available_slots_for_doctor_on_date(
                    doctor,
                    direction,
                    target_date,
                )

                self.fields["appointment_time"].choices = [
                    ("", "Оберіть час"),
                    *[(slot["value"], slot["label"]) for slot in slots],
                ]
            except (Doctor.DoesNotExist, Direction.DoesNotExist, ValidationError):
                pass

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        direction = cleaned_data.get("direction")
        doctor = cleaned_data.get("doctor")
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")

        today = timezone.localdate()

        if appointment_date and appointment_date < today:
            raise ValidationError("Не можна обрати минулу дату.")

        if direction and doctor and not doctor.directions.filter(id=direction.id).exists():
            raise ValidationError("Обраний лікар не працює в цьому напрямі.")

        if doctor and direction and appointment_date:
            available_dates = get_available_dates_for_doctor_direction(
                doctor,
                direction,
            )
            if appointment_date.strftime("%Y-%m-%d") not in available_dates:
                raise ValidationError("На цю дату запис недоступний.")

        if doctor and direction and appointment_date and appointment_time:
            slots = get_available_slots_for_doctor_on_date(
                doctor,
                direction,
                appointment_date,
            )

            available_values = {slot["value"] for slot in slots}

            if appointment_time not in available_values:
                raise ValidationError("Цей часовий слот уже недоступний.")

            cleaned_data["appointment_time"] = datetime.strptime(
                appointment_time,
                "%H:%M",
            ).time()

        return cleaned_data


class GuestAppointmentCreateForm(AppointmentCreateForm):
    last_name = forms.CharField(
        label="Прізвище",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="Імʼя",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    middle_name = forms.CharField(
        label="По батькові",
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta(AppointmentCreateForm.Meta):
        fields = (
            "last_name",
            "first_name",
            "middle_name",
            "phone",
            "email",
            "direction",
            "doctor",
            "appointment_date",
            "appointment_time",
            "description",
        )


class SupportAppointmentCreateForm(AppointmentCreateForm):
    user = forms.ModelChoiceField(
        queryset=patient_users_queryset().order_by("last_name", "first_name"),
        required=False,
        label="Зареєстрований користувач",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    last_name = forms.CharField(
        required=False,
        label="Прізвище",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        required=False,
        label="Імʼя",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    middle_name = forms.CharField(
        required=False,
        label="По батькові",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        required=False,
        label="Телефон",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta(AppointmentCreateForm.Meta):
        fields = (
            "user",
            "last_name",
            "first_name",
            "middle_name",
            "phone",
            "email",
            "direction",
            "doctor",
            "appointment_date",
            "appointment_time",
            "description",
        )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        user = cleaned_data.get("user")

        last_name = (cleaned_data.get("last_name") or "").strip()
        first_name = (cleaned_data.get("first_name") or "").strip()
        middle_name = (cleaned_data.get("middle_name") or "").strip()
        phone = (cleaned_data.get("phone") or "").strip()
        email = (cleaned_data.get("email") or "").strip()

        guest_fields_filled = any([last_name, first_name, middle_name, phone, email])

        # 1. Не можна одночасно вибрати користувача і вводити дані незареєстрованого
        if user and guest_fields_filled:
            raise ValidationError(
                "Оберіть або зареєстрованого користувача, або заповніть дані незареєстрованого пацієнта."
            )

        # 2. Має бути обраний один зі сценаріїв
        if not user and not guest_fields_filled:
            raise ValidationError(
                "Оберіть зареєстрованого користувача або заповніть дані незареєстрованого пацієнта."
            )

        # 3. Якщо користувача не вибрано — обов’язкові дані гостя
        if not user:
            if not all([last_name, first_name, phone, email]):
                raise ValidationError(
                    "Для незареєстрованого пацієнта потрібно заповнити прізвище, імʼя, телефон і email."
                )

            cleaned_data["last_name"] = last_name
            cleaned_data["first_name"] = first_name
            cleaned_data["middle_name"] = middle_name
            cleaned_data["phone"] = phone
            cleaned_data["email"] = email

        return cleaned_data

class SupportAppointmentUpdateForm(forms.ModelForm):
    appointment_date = forms.DateField(
        required=True,
        label="Дата прийому",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Оберіть дату",
            }
        ),
    )

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
            "status",
            "rejection_reason",
            "final_conclusion",
        )
        widgets = {
            "direction": forms.Select(attrs={"class": "form-select"}),
            "doctor": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "rejection_reason": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "final_conclusion": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        is_rejected = self.instance and self.instance.status == AppointmentStatus.REJECTED
        is_completed = self.instance and self.instance.status == AppointmentStatus.COMPLETED

        self.fields["doctor"].queryset = Doctor.objects.none()
        self.fields["appointment_time"].choices = [("", "Оберіть час")]

        direction_id = self.data.get("direction") or getattr(self.instance.direction, "id", None)
        doctor_id = self.data.get("doctor") or getattr(self.instance.doctor, "id", None)
        appointment_date = self.data.get("appointment_date") or (
            self.instance.appointment_date.strftime("%Y-%m-%d")
            if self.instance and self.instance.appointment_date
            else None
        )

        if direction_id:
            self.fields["doctor"].queryset = (
                Doctor.objects.filter(directions__id=direction_id)
                .distinct()
                .order_by("last_name", "first_name")
            )

        if direction_id and doctor_id and appointment_date:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                direction = Direction.objects.get(id=direction_id)
                target_date = forms.DateField().clean(appointment_date)

                slots = get_available_slots_for_doctor_on_date(
                    doctor,
                    direction,
                    target_date,
                    exclude_appointment_id=self.instance.id if self.instance else None,
                )

                self.fields["appointment_time"].choices = [
                    ("", "Оберіть час"),
                    *[(slot["value"], slot["label"]) for slot in slots],
                ]

                current_time_value = (
                    self.instance.appointment_time.strftime("%H:%M")
                    if self.instance and self.instance.appointment_time
                    else None
                )

                if current_time_value and current_time_value not in [value for value, _ in self.fields["appointment_time"].choices]:
                    self.fields["appointment_time"].choices.append(
                        (current_time_value, f"{current_time_value} - поточний слот")
                    )

            except (Doctor.DoesNotExist, Direction.DoesNotExist, ValidationError):
                pass

        if is_rejected:
            for field_name in (
                "direction",
                "doctor",
                "appointment_date",
                "appointment_time",
                "description",
                "status",
                "rejection_reason",
                "final_conclusion",
            ):
                if field_name in self.fields:
                    self.fields[field_name].disabled = True

        if is_completed:
            for field_name in (
                "direction",
                "doctor",
                "appointment_date",
                "appointment_time",
                "description",
                "status",
                "rejection_reason",
            ):
                if field_name in self.fields:
                    self.fields[field_name].disabled = True

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        if self.instance and self.instance.status == AppointmentStatus.REJECTED:
            return cleaned_data

        if self.instance and self.instance.status == AppointmentStatus.COMPLETED:
            cleaned_data["direction"] = self.instance.direction
            cleaned_data["doctor"] = self.instance.doctor
            cleaned_data["appointment_date"] = self.instance.appointment_date
            cleaned_data["appointment_time"] = self.instance.appointment_time
            cleaned_data["description"] = self.instance.description
            cleaned_data["status"] = self.instance.status
            cleaned_data["rejection_reason"] = self.instance.rejection_reason
            return cleaned_data

        direction = cleaned_data.get("direction")
        doctor = cleaned_data.get("doctor")
        appointment_date = cleaned_data.get("appointment_date")
        appointment_time = cleaned_data.get("appointment_time")
        status = cleaned_data.get("status")
        rejection_reason = cleaned_data.get("rejection_reason", "")
        final_conclusion = cleaned_data.get("final_conclusion")

        today = timezone.localdate()

        if appointment_date and appointment_date < today:
            raise ValidationError("Не можна обрати минулу дату.")

        if direction and doctor and not doctor.directions.filter(id=direction.id).exists():
            raise ValidationError("Обраний лікар не працює в цьому напрямі.")

        if doctor and direction and appointment_date:
            available_dates = get_available_dates_for_doctor_direction(
                doctor,
                direction,
                exclude_appointment_id=self.instance.id if self.instance else None,
            )

            current_instance_date = (
                self.instance.appointment_date.strftime("%Y-%m-%d")
                if self.instance and self.instance.appointment_date
                else None
            )

            selected_date_str = appointment_date.strftime("%Y-%m-%d")

            if selected_date_str not in available_dates:
                same_current_slot = (
                    self.instance
                    and selected_date_str == current_instance_date
                    and doctor == self.instance.doctor
                    and direction == self.instance.direction
                )
                if not same_current_slot:
                    raise ValidationError("На цю дату запис недоступний.")

        if doctor and direction and appointment_date and appointment_time:
            slots = get_available_slots_for_doctor_on_date(
                doctor,
                direction,
                appointment_date,
                exclude_appointment_id=self.instance.id if self.instance else None,
            )

            available_values = {slot["value"] for slot in slots}

            current_instance_time = (
                self.instance.appointment_time.strftime("%H:%M")
                if self.instance and self.instance.appointment_time
                else None
            )
            current_instance_date = (
                self.instance.appointment_date
                if self.instance
                else None
            )
            current_instance_doctor = self.instance.doctor if self.instance else None
            current_instance_direction = self.instance.direction if self.instance else None

            same_current_slot = (
                self.instance
                and appointment_time == current_instance_time
                and appointment_date == current_instance_date
                and doctor == current_instance_doctor
                and direction == current_instance_direction
            )

            if appointment_time not in available_values and not same_current_slot:
                raise ValidationError("Цей часовий слот уже недоступний.")

            cleaned_data["appointment_time"] = datetime.strptime(
                appointment_time,
                "%H:%M",
            ).time()

        if status == AppointmentStatus.REJECTED and not rejection_reason.strip():
            self.add_error("rejection_reason", "Вкажіть причину відхилення.")

        if status == AppointmentStatus.COMPLETED and not final_conclusion and not self.instance.final_conclusion:
            self.add_error("final_conclusion", "Додайте висновок лікаря.")

        return cleaned_data