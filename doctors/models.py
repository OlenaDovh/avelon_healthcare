"""Модуль doctors/models.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Direction(models.Model):
    """Клас Direction.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    name = models.CharField(max_length=255, unique=True, verbose_name='Назва напряму')
    description = models.TextField(verbose_name='Опис напряму')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Напрям'
        verbose_name_plural = 'Напрями'
        ordering = ['name']

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return str(self.name)

class Doctor(models.Model):
    """Клас Doctor.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    user: models.OneToOneField = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='doctor_profile', null=True, blank=True, verbose_name='Користувач')
    last_name: models.CharField = models.CharField(max_length=150, verbose_name='Прізвище')
    first_name: models.CharField = models.CharField(max_length=150, verbose_name="Ім'я")
    middle_name: models.CharField = models.CharField(max_length=150, blank=True, verbose_name='По батькові')
    position: models.CharField = models.CharField(max_length=255, verbose_name='Посада')
    directions = models.ManyToManyField(Direction, related_name='doctors', verbose_name='Напрями')
    qualification_category: models.CharField = models.CharField(max_length=255, verbose_name='Кваліфікаційна категорія')
    experience_years: models.PositiveIntegerField = models.PositiveIntegerField(verbose_name='Стаж (років)')
    price_from: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна від')
    price_to: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна до')
    photo: models.ImageField = models.ImageField(upload_to='doctors/photos/', blank=True, null=True, verbose_name='Фото')
    work_experience_description: models.TextField = models.TextField(blank=True, verbose_name='Досвід роботи')
    when_to_contact: models.TextField = models.TextField(blank=True, verbose_name='У яких випадках звертатись')
    education: models.TextField = models.TextField(blank=True, verbose_name='Освіта')
    licenses: models.ImageField = models.ImageField(upload_to='doctors/licenses/', blank=True, null=True, verbose_name='Ліцензії / фото ліцензій')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Лікар'
        verbose_name_plural = 'Лікарі'
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self) -> str:
        """Виконує логіку `full_name`.

Returns:
    Результат виконання операції."""
        return ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return self.full_name

class DoctorWorkDay(models.Model):
    """Клас DoctorWorkDay.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    APPOINTMENT_DURATION_CHOICES = ((15, '15 хв'), (30, '30 хв'), (60, '60 хв'))
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='workdays', verbose_name='Лікар')
    work_date = models.DateField(verbose_name='Дата роботи')
    appointment_duration_minutes = models.PositiveSmallIntegerField(choices=APPOINTMENT_DURATION_CHOICES, default=30, verbose_name='Тривалість 1 прийому')
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='doctor_workdays', verbose_name='Напрям')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Розклад лікаря на дату'
        verbose_name_plural = 'Розклад лікарів на дати'
        ordering = ['-work_date', 'doctor__last_name', 'doctor__first_name']
        constraints = [models.UniqueConstraint(fields=['doctor', 'direction', 'work_date'], name='unique_doctor_direction_work_date')]

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return f'{self.doctor.full_name} — {self.work_date}'

    def clean(self) -> None:
        """Виконує логіку `clean`.

Returns:
    None."""
        if self.work_date and self.work_date < timezone.localdate():
            raise ValidationError('Не можна створити графік на минулу дату.')
        if self.doctor_id and self.direction_id:
            if not self.doctor.directions.filter(id=self.direction_id).exists():
                raise ValidationError('Обраний лікар не має цього напряму.')

    def save(self, *args: object, **kwargs: object) -> None:
        """Виконує логіку `save`.

Args:
    args: Вхідне значення для виконання операції.
    kwargs: Вхідне значення для виконання операції.

Returns:
    None."""
        self.full_clean()
        super().save(*args, **kwargs)

class DoctorWorkPeriod(models.Model):
    """Клас DoctorWorkPeriod.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    workday = models.ForeignKey(DoctorWorkDay, on_delete=models.CASCADE, related_name='periods', verbose_name='Робочий день')
    start_time = models.TimeField(verbose_name='Початок періоду')
    end_time = models.TimeField(verbose_name='Кінець періоду')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Робочий період'
        verbose_name_plural = 'Робочі періоди'
        ordering = ['start_time']

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return f'{self.start_time} - {self.end_time}'

    def get_slots(self) -> list[tuple[datetime, datetime]]:
        """Виконує логіку `get_slots`.

Returns:
    Результат виконання операції."""
        result: list[tuple[datetime, datetime]] = []
        duration = timedelta(minutes=self.workday.appointment_duration_minutes)
        current = datetime.combine(self.workday.work_date, self.start_time)
        end_dt = datetime.combine(self.workday.work_date, self.end_time)
        while current + duration <= end_dt:
            result.append((current, current + duration))
            current += duration
        return result

    def clean(self) -> None:
        """Виконує логіку `clean`.

Returns:
    None."""
        super().clean()
        self._validate_time_order()
        self._validate_overlap()

    def _validate_time_order(self) -> None:
        """Виконує логіку `_validate_time_order`.

Returns:
    None."""
        if not self.start_time or not self.end_time:
            return
        if self.start_time >= self.end_time:
            raise ValidationError('Час початку періоду має бути меншим за час завершення.')

    def _validate_overlap(self) -> None:
        """Виконує логіку `_validate_overlap`.

Returns:
    None."""
        if not self.start_time or not self.end_time or (not self.workday_id):
            return
        overlapping_periods = DoctorWorkPeriod.objects.filter(workday_id=self.workday_id).exclude(pk=self.pk)
        for period in overlapping_periods:
            if self.start_time < period.end_time and self.end_time > period.start_time:
                raise ValidationError('Цей період перетинається з іншим періодом роботи лікаря.')

    def save(self, *args: object, **kwargs: object) -> None:
        """Виконує логіку `save`.

Args:
    args: Вхідне значення для виконання операції.
    kwargs: Вхідне значення для виконання операції.

Returns:
    None."""
        self.full_clean()
        super().save(*args, **kwargs)
