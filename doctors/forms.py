from __future__ import annotations

from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

from .models import Direction, Doctor, DoctorWorkDay, DoctorWorkPeriod

User = get_user_model()


class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ("name", "description")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class DoctorForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.filter(
            groups__name="doctor"
        ).distinct().order_by("last_name", "first_name", "username")

        self.fields["user"].label_from_instance = lambda obj: (
                obj.get_full_name() or obj.username
        )


class DoctorWorkDayForm(forms.ModelForm):
    class Meta:
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["doctor"].queryset = Doctor.objects.prefetch_related("directions").order_by(
            "last_name", "first_name"
        )

        self.fields["direction"].queryset = Direction.objects.none()

        doctor_id = self.data.get("doctor") or getattr(self.instance, "doctor_id", None)

        if doctor_id:
            self.fields["direction"].queryset = Direction.objects.filter(
                doctors__id=doctor_id
            ).distinct().order_by("name")
        elif self.instance.pk and self.instance.doctor_id:
            self.fields["direction"].queryset = self.instance.doctor.directions.all().order_by("name")


class DoctorWorkPeriodForm(forms.ModelForm):
    class Meta:
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
