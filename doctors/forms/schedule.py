"""Модуль doctors/forms/schedule.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from typing import Any
from django import forms
from django.forms import inlineformset_factory
from doctors.models import Direction, Doctor, DoctorWorkDay, DoctorWorkPeriod

class DoctorWorkDayForm(forms.ModelForm):
    """Клас DoctorWorkDayForm.

Відповідає за поведінку, описану в цьому компоненті застосунку."""

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        model = DoctorWorkDay
        fields = ('doctor', 'direction', 'work_date', 'appointment_duration_minutes')
        widgets = {'doctor': forms.Select(attrs={'class': 'form-select'}), 'direction': forms.Select(attrs={'class': 'form-select'}), 'work_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 'appointment_duration_minutes': forms.Select(attrs={'class': 'form-select'})}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Виконує логіку `__init__`.

Args:
    args: Вхідне значення для виконання операції.
    kwargs: Вхідне значення для виконання операції.

Returns:
    None."""
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.prefetch_related('directions').order_by('last_name', 'first_name')
        self.fields['direction'].queryset = Direction.objects.none()
        doctor_id = self.data.get('doctor') or getattr(self.instance, 'doctor_id', None)
        if doctor_id:
            self.fields['direction'].queryset = Direction.objects.filter(doctors__id=doctor_id).distinct().order_by('name')
        elif self.instance.pk and self.instance.doctor_id:
            self.fields['direction'].queryset = self.instance.doctor.directions.all().order_by('name')

class DoctorWorkPeriodForm(forms.ModelForm):
    """Клас DoctorWorkPeriodForm.

Відповідає за поведінку, описану в цьому компоненті застосунку."""

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        model = DoctorWorkPeriod
        fields = ('start_time', 'end_time')
        widgets = {'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}), 'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})}
DoctorWorkPeriodFormSet = inlineformset_factory(DoctorWorkDay, DoctorWorkPeriod, form=DoctorWorkPeriodForm, extra=1, can_delete=False)
