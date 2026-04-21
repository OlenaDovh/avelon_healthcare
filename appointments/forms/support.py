from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError

from accounts.selectors import patient_users_queryset
from appointments.forms.create import AppointmentCreateForm


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

    def clean(self) -> dict:
        cleaned_data = super().clean()

        user = cleaned_data.get("user")
        last_name = (cleaned_data.get("last_name") or "").strip()
        first_name = (cleaned_data.get("first_name") or "").strip()
        middle_name = (cleaned_data.get("middle_name") or "").strip()
        phone = (cleaned_data.get("phone") or "").strip()
        email = (cleaned_data.get("email") or "").strip()

        guest_fields_filled = any([last_name, first_name, middle_name, phone, email])

        if user and guest_fields_filled:
            raise ValidationError(
                "Оберіть або зареєстрованого користувача, або заповніть дані незареєстрованого пацієнта."
            )

        if not user and not guest_fields_filled:
            raise ValidationError(
                "Оберіть зареєстрованого користувача або заповніть дані незареєстрованого пацієнта."
            )

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