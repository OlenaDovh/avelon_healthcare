from __future__ import annotations
from typing import Any
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import Direction, Doctor, DoctorWorkDay, DoctorWorkPeriod

class DoctorWorkPeriodInlineFormSet(BaseInlineFormSet):
    """Описує клас `DoctorWorkPeriodInlineFormSet`."""

    def clean(self) -> None:
        """Виконує логіку `clean`.

Returns:
    Any: Результат виконання."""
        super().clean()
        periods = []
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            if not start_time or not end_time:
                continue
            if start_time >= end_time:
                raise ValidationError('Час початку періоду має бути меншим за час завершення.')
            for existing_start, existing_end in periods:
                if start_time < existing_end and end_time > existing_start:
                    raise ValidationError('Періоди роботи не можуть перетинатися між собою.')
            periods.append((start_time, end_time))

class DoctorWorkPeriodInline(admin.TabularInline):
    """Описує клас `DoctorWorkPeriodInline`."""
    model = DoctorWorkPeriod
    extra = 1
    formset = DoctorWorkPeriodInlineFormSet

class DoctorWorkDayInlineForm(forms.ModelForm):
    """Описує клас `DoctorWorkDayInlineForm`."""

    class Meta:
        """Описує клас `Meta`."""
        model = DoctorWorkDay
        fields = '__all__'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Виконує логіку `__init__`.

Args:
    *args: Вхідний параметр `args`.
    **kwargs: Вхідний параметр `kwargs`.

Returns:
    Any: Результат виконання."""
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.doctor_id:
            self.fields['direction'].queryset = self.instance.doctor.directions.all().order_by('name')
        elif self.initial.get('doctor'):
            doctor = self.initial['doctor']
            self.fields['direction'].queryset = doctor.directions.all().order_by('name')
        else:
            self.fields['direction'].queryset = Direction.objects.none()

class DoctorWorkDayInline(admin.StackedInline):
    """Описує клас `DoctorWorkDayInline`."""
    model = DoctorWorkDay
    extra = 0
    form = DoctorWorkDayInlineForm
    show_change_link = True

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    """Описує клас `DirectionAdmin`."""
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Описує клас `DoctorAdmin`."""
    list_display = ('full_name', 'position', 'qualification_category', 'experience_years', 'price_from', 'price_to')
    search_fields = ('full_name', 'position')
    list_filter = ('position', 'qualification_category', 'directions')
    filter_horizontal = ('directions',)
    inlines = [DoctorWorkDayInline]

@admin.register(DoctorWorkDay)
class DoctorWorkDayAdmin(admin.ModelAdmin):
    """Описує клас `DoctorWorkDayAdmin`."""
    list_display = ('doctor', 'direction', 'work_date', 'appointment_duration_minutes')
    list_filter = ('work_date', 'direction', 'appointment_duration_minutes', 'doctor')
    search_fields = ('doctor__full_name', 'direction__name')
    inlines = [DoctorWorkPeriodInline]
