"""Модуль `doctors/admin.py` застосунку `doctors`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations
from typing import Any

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from .models import Direction, Doctor, DoctorWorkDay, DoctorWorkPeriod


class DoctorWorkPeriodInlineFormSet(BaseInlineFormSet):
    """Клас `DoctorWorkPeriodInlineFormSet` інкапсулює повʼязану логіку проєкту.

    Базові класи: `BaseInlineFormSet`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    def clean(self) -> None:
        """Перевіряє, очищує та нормалізує введені дані.

        Повертає:
            None: Функція виконує дію без явного значення результату.
        """
        super().clean()

        periods = []

        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue

            start_time = form.cleaned_data.get("start_time")
            end_time = form.cleaned_data.get("end_time")

            if not start_time or not end_time:
                continue

            if start_time >= end_time:
                raise ValidationError(
                    "Час початку періоду має бути меншим за час завершення."
                )

            for existing_start, existing_end in periods:
                if start_time < existing_end and end_time > existing_start:
                    raise ValidationError(
                        "Періоди роботи не можуть перетинатися між собою."
                    )

            periods.append((start_time, end_time))


class DoctorWorkPeriodInline(admin.TabularInline):
    """Клас `DoctorWorkPeriodInline` інкапсулює повʼязану логіку проєкту.

    Базові класи: `admin.TabularInline`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    model = DoctorWorkPeriod
    extra = 1
    formset = DoctorWorkPeriodInlineFormSet


class DoctorWorkDayInlineForm(forms.ModelForm):
    """Клас `DoctorWorkDayInlineForm` інкапсулює повʼязану логіку проєкту.

    Базові класи: `forms.ModelForm`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    class Meta:
        """Клас `Meta` інкапсулює повʼязану логіку проєкту.

        Базові класи: `object`.
        Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
        """
        model = DoctorWorkDay
        fields = "__all__"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Ініціалізує обʼєкт і встановлює початковий стан.

        Параметри:
            *args: Значення типу `Any`, яке передається для виконання логіки функції.
            **kwargs: Значення типу `Any`, яке передається для виконання логіки функції.

        Повертає:
            None: Функція виконує дію без явного значення результату.
        """
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.doctor_id:
            self.fields["direction"].queryset = self.instance.doctor.directions.all().order_by("name")
        elif self.initial.get("doctor"):
            doctor = self.initial["doctor"]
            self.fields["direction"].queryset = doctor.directions.all().order_by("name")
        else:
            self.fields["direction"].queryset = Direction.objects.none()


class DoctorWorkDayInline(admin.StackedInline):
    """Клас `DoctorWorkDayInline` інкапсулює повʼязану логіку проєкту.

    Базові класи: `admin.StackedInline`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    model = DoctorWorkDay
    extra = 0
    form = DoctorWorkDayInlineForm
    show_change_link = True


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    """Клас `DirectionAdmin` інкапсулює повʼязану логіку проєкту.

    Базові класи: `admin.ModelAdmin`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Клас `DoctorAdmin` інкапсулює повʼязану логіку проєкту.

    Базові класи: `admin.ModelAdmin`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    list_display = (
        "full_name",
        "position",
        "qualification_category",
        "experience_years",
        "price_from",
        "price_to",
    )
    search_fields = ("full_name", "position")
    list_filter = ("position", "qualification_category", "directions")
    filter_horizontal = ("directions",)
    inlines = [DoctorWorkDayInline]


@admin.register(DoctorWorkDay)
class DoctorWorkDayAdmin(admin.ModelAdmin):
    """Клас `DoctorWorkDayAdmin` інкапсулює повʼязану логіку проєкту.

    Базові класи: `admin.ModelAdmin`.
    Використовується для опису доменної сутності, форми, адміністративної конфігурації, сервісу або представлення залежно від місця використання.
    """
    list_display = (
        "doctor",
        "direction",
        "work_date",
        "appointment_duration_minutes",
    )
    list_filter = (
        "work_date",
        "direction",
        "appointment_duration_minutes",
        "doctor",
    )
    search_fields = ("doctor__full_name", "direction__name")
    inlines = [DoctorWorkPeriodInline]
