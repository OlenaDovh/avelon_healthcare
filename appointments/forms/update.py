"""Модуль appointments/forms/update.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from datetime import datetime
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from appointments.models import Appointment, AppointmentStatus
from doctors.models import Direction, Doctor
from appointments.services import get_available_dates_for_doctor_direction, get_available_slots_for_doctor_on_date

class SupportAppointmentUpdateForm(forms.ModelForm):
    """Клас SupportAppointmentUpdateForm.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    appointment_date = forms.DateField(required=True, label='Дата прийому', widget=forms.DateInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Оберіть дату'}))
    appointment_time = forms.ChoiceField(required=True, label='Час прийому', widget=forms.Select(attrs={'class': 'form-select'}), choices=[('', 'Оберіть час')])

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        model = Appointment
        fields = ('direction', 'doctor', 'appointment_date', 'appointment_time', 'description', 'status', 'rejection_reason', 'final_conclusion')
        widgets = {'direction': forms.Select(attrs={'class': 'form-select'}), 'doctor': forms.Select(attrs={'class': 'form-select'}), 'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 'status': forms.Select(attrs={'class': 'form-select'}), 'rejection_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 'final_conclusion': forms.ClearableFileInput(attrs={'class': 'form-control'})}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Виконує логіку `__init__`.

Args:
    args: Вхідне значення для виконання операції.
    kwargs: Вхідне значення для виконання операції.

Returns:
    None."""
        super().__init__(*args, **kwargs)
        is_rejected = self.instance and self.instance.status == AppointmentStatus.REJECTED
        is_completed = self.instance and self.instance.status == AppointmentStatus.COMPLETED
        self.fields['doctor'].queryset = Doctor.objects.none()
        self.fields['appointment_time'].choices = [('', 'Оберіть час')]
        direction_id = self.data.get('direction') or getattr(self.instance.direction, 'id', None)
        doctor_id = self.data.get('doctor') or getattr(self.instance.doctor, 'id', None)
        appointment_date = self.data.get('appointment_date') or (self.instance.appointment_date.strftime('%Y-%m-%d') if self.instance and self.instance.appointment_date else None)
        if direction_id:
            self.fields['doctor'].queryset = Doctor.objects.filter(directions__id=direction_id).distinct().order_by('last_name', 'first_name')
        if direction_id and doctor_id and appointment_date:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                direction = Direction.objects.get(id=direction_id)
                target_date = forms.DateField().clean(appointment_date)
                slots = get_available_slots_for_doctor_on_date(doctor, direction, target_date, exclude_appointment_id=self.instance.id if self.instance else None)
                self.fields['appointment_time'].choices = [('', 'Оберіть час'), *[(slot['value'], slot['label']) for slot in slots]]
                current_time_value = self.instance.appointment_time.strftime('%H:%M') if self.instance and self.instance.appointment_time else None
                if current_time_value and current_time_value not in [value for value, _ in self.fields['appointment_time'].choices]:
                    self.fields['appointment_time'].choices.append((current_time_value, f'{current_time_value} - поточний слот'))
            except (Doctor.DoesNotExist, Direction.DoesNotExist, ValidationError):
                pass
        if is_rejected:
            for field_name in ('direction', 'doctor', 'appointment_date', 'appointment_time', 'description', 'status', 'rejection_reason', 'final_conclusion'):
                if field_name in self.fields:
                    self.fields[field_name].disabled = True
        if is_completed:
            for field_name in ('direction', 'doctor', 'appointment_date', 'appointment_time', 'description', 'status', 'rejection_reason'):
                if field_name in self.fields:
                    self.fields[field_name].disabled = True

    def clean(self) -> dict[str, Any]:
        """Виконує логіку `clean`.

Returns:
    Результат виконання операції."""
        cleaned_data = super().clean()
        if self.instance and self.instance.status == AppointmentStatus.REJECTED:
            return cleaned_data
        if self.instance and self.instance.status == AppointmentStatus.COMPLETED:
            cleaned_data['direction'] = self.instance.direction
            cleaned_data['doctor'] = self.instance.doctor
            cleaned_data['appointment_date'] = self.instance.appointment_date
            cleaned_data['appointment_time'] = self.instance.appointment_time
            cleaned_data['description'] = self.instance.description
            cleaned_data['status'] = self.instance.status
            cleaned_data['rejection_reason'] = self.instance.rejection_reason
            return cleaned_data
        direction = cleaned_data.get('direction')
        doctor = cleaned_data.get('doctor')
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        status = cleaned_data.get('status')
        rejection_reason = cleaned_data.get('rejection_reason', '')
        final_conclusion = cleaned_data.get('final_conclusion')
        today = timezone.localdate()
        if appointment_date and appointment_date < today:
            raise ValidationError('Не можна обрати минулу дату.')
        if direction and doctor and (not doctor.directions.filter(id=direction.id).exists()):
            raise ValidationError('Обраний лікар не працює в цьому напрямі.')
        if doctor and direction and appointment_date:
            available_dates = get_available_dates_for_doctor_direction(doctor, direction, exclude_appointment_id=self.instance.id if self.instance else None)
            current_instance_date = self.instance.appointment_date.strftime('%Y-%m-%d') if self.instance and self.instance.appointment_date else None
            selected_date_str = appointment_date.strftime('%Y-%m-%d')
            if selected_date_str not in available_dates:
                same_current_slot = self.instance and selected_date_str == current_instance_date and (doctor == self.instance.doctor) and (direction == self.instance.direction)
                if not same_current_slot:
                    raise ValidationError('На цю дату запис недоступний.')
        if doctor and direction and appointment_date and appointment_time:
            slots = get_available_slots_for_doctor_on_date(doctor, direction, appointment_date, exclude_appointment_id=self.instance.id if self.instance else None)
            available_values = {slot['value'] for slot in slots}
            current_instance_time = self.instance.appointment_time.strftime('%H:%M') if self.instance and self.instance.appointment_time else None
            current_instance_date = self.instance.appointment_date if self.instance else None
            current_instance_doctor = self.instance.doctor if self.instance else None
            current_instance_direction = self.instance.direction if self.instance else None
            same_current_slot = self.instance and appointment_time == current_instance_time and (appointment_date == current_instance_date) and (doctor == current_instance_doctor) and (direction == current_instance_direction)
            if appointment_time not in available_values and (not same_current_slot):
                raise ValidationError('Цей часовий слот уже недоступний.')
            cleaned_data['appointment_time'] = datetime.strptime(appointment_time, '%H:%M').time()
        if status == AppointmentStatus.REJECTED and (not rejection_reason.strip()):
            self.add_error('rejection_reason', 'Вкажіть причину відхилення.')
        if status == AppointmentStatus.COMPLETED and (not final_conclusion) and (not self.instance.final_conclusion):
            self.add_error('final_conclusion', 'Додайте висновок лікаря.')
        return cleaned_data
