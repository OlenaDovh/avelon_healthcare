from __future__ import annotations
from datetime import datetime
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils import timezone
from doctors.models import Direction, Doctor
from appointments.models import Appointment
from appointments.services import get_available_dates_for_doctor_direction, get_available_slots_for_doctor_on_date

class AppointmentCreateForm(forms.ModelForm):
    """Описує клас `AppointmentCreateForm`."""
    appointment_date = forms.DateField(required=True, label='Дата прийому', widget=forms.DateInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Оберіть дату'}))
    appointment_time = forms.ChoiceField(required=True, label='Час прийому', widget=forms.Select(attrs={'class': 'form-select'}), choices=[('', 'Оберіть час')])

    class Meta:
        """Описує клас `Meta`."""
        model = Appointment
        fields = ('direction', 'doctor', 'appointment_date', 'appointment_time', 'description')
        widgets = {'direction': forms.Select(attrs={'class': 'form-select'}), 'doctor': forms.Select(attrs={'class': 'form-select'}), 'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишіть причину звернення до лікаря'})}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Виконує логіку `__init__`.

Args:
    *args: Вхідний параметр `args`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        super().__init__(*args, **kwargs)
        self.fields['direction'].queryset = Direction.objects.annotate(doctors_count=Count('doctors')).filter(doctors_count__gt=0).order_by('name')
        self.fields['doctor'].queryset = Doctor.objects.none()
        self.fields['appointment_time'].choices = [('', 'Оберіть час')]
        direction_id = self.data.get('direction') or self.initial.get('direction')
        doctor_id = self.data.get('doctor') or self.initial.get('doctor')
        appointment_date = self.data.get('appointment_date') or self.initial.get('appointment_date')
        if direction_id:
            self.fields['doctor'].queryset = Doctor.objects.filter(directions__id=direction_id).distinct().order_by('last_name', 'first_name')
        if direction_id and doctor_id and appointment_date:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                direction = Direction.objects.get(id=direction_id)
                target_date = forms.DateField().clean(appointment_date)
                slots = get_available_slots_for_doctor_on_date(doctor, direction, target_date)
                self.fields['appointment_time'].choices = [('', 'Оберіть час'), *[(slot['value'], slot['label']) for slot in slots]]
            except (Doctor.DoesNotExist, Direction.DoesNotExist, ValidationError):
                pass

    def clean(self) -> dict[str, Any]:
        """Виконує логіку `clean`.

Returns:
    Any: Результат виконання."""
        cleaned_data = super().clean()
        direction = cleaned_data.get('direction')
        doctor = cleaned_data.get('doctor')
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        today = timezone.localdate()
        if appointment_date and appointment_date < today:
            raise ValidationError('Не можна обрати минулу дату.')
        if direction and doctor and (not doctor.directions.filter(id=direction.id).exists()):
            raise ValidationError('Обраний лікар не працює в цьому напрямі.')
        if doctor and direction and appointment_date:
            available_dates = get_available_dates_for_doctor_direction(doctor, direction)
            if appointment_date.strftime('%Y-%m-%d') not in available_dates:
                raise ValidationError('На цю дату запис недоступний.')
        if doctor and direction and appointment_date and appointment_time:
            slots = get_available_slots_for_doctor_on_date(doctor, direction, appointment_date)
            available_values = {slot['value'] for slot in slots}
            if appointment_time not in available_values:
                raise ValidationError('Цей часовий слот уже недоступний.')
            cleaned_data['appointment_time'] = datetime.strptime(appointment_time, '%H:%M').time()
        return cleaned_data

class GuestAppointmentCreateForm(AppointmentCreateForm):
    """Описує клас `GuestAppointmentCreateForm`."""
    last_name = forms.CharField(label='Прізвище', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Імʼя', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(label='По батькові', required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta(AppointmentCreateForm.Meta):
        """Описує клас `Meta`."""
        fields = ('last_name', 'first_name', 'middle_name', 'phone', 'email', 'direction', 'doctor', 'appointment_date', 'appointment_time', 'description')
