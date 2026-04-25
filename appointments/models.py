from __future__ import annotations
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from doctors.models import Direction, Doctor, DoctorWorkDay


class AppointmentStatus(models.TextChoices):
    """
    Перелік статусів запису до лікаря.
    """

    PLANNED = "planned", "Заплановано"
    COMPLETED = "completed", "Завершено"
    REJECTED = "rejected", "Відхилено"


class Appointment(models.Model):
    """
    Модель запису пацієнта до лікаря.

    Зберігає дані пацієнта, лікаря, напряму, часу прийому та статусу запису.
    """

    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Користувач",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=150, verbose_name="Прізвище"
    )
    first_name = models.CharField(
        max_length=150, verbose_name="Імʼя"
    )
    middle_name = models.CharField(
        max_length=150, blank=True, verbose_name="По батькові"
    )
    phone: models.CharField = models.CharField(
        max_length=30,
        verbose_name="Телефон",
        blank=True,
        default="",
    )
    email: models.EmailField = models.EmailField(
        verbose_name="Email",
        blank=True,
        default="",
    )
    direction: models.ForeignKey = models.ForeignKey(
        Direction,
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Напрям",
    )
    doctor: models.ForeignKey = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Лікар",
    )
    appointment_date: models.DateField = models.DateField(
        verbose_name="Дата прийому",
    )
    appointment_time: models.TimeField = models.TimeField(
        verbose_name="Час прийому",
    )
    description: models.TextField = models.TextField(
        blank=True,
        verbose_name="Опис причини звернення",
    )
    status: models.CharField = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PLANNED,
        verbose_name="Статус",
    )
    rejection_reason: models.TextField = models.TextField(
        blank=True,
        verbose_name="Причина відхилення",
    )
    final_conclusion: models.FileField = models.FileField(
        upload_to="appointments/conclusions/",
        blank=True,
        null=True,
        verbose_name="Висновок лікаря (PDF)",
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення",
    )

    class Meta:
        """
        Метадані моделі запису до лікаря.

        Визначає назви, сортування та унікальність слота прийому.
        """

        verbose_name = "Запис до лікаря"
        verbose_name_plural = "Записи до лікаря"
        ordering = ["-appointment_date", "-appointment_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date", "appointment_time"],
                name="unique_doctor_appointment_slot",
            )
        ]

    def clean(self) -> None:
        """
        Перевіряє коректність запису до лікаря.

        Raises:
            ValidationError: Якщо лікар не належить до вибраного напряму
                або не вказана причина відхилення.
        """
        super().clean()

        if self.doctor_id and self.direction_id:
            if not self.doctor.directions.filter(id=self.direction_id).exists():
                raise ValidationError(
                    {"doctor": "Обраний лікар не працює в цьому напрямі."}
                )

        if self.status == AppointmentStatus.REJECTED and not self.rejection_reason.strip():
            raise ValidationError(
                {"rejection_reason": "Вкажіть причину відхилення."}
            )

    @property
    def customer_name(self) -> str:
        """
        Повертає ім'я пацієнта.

        Returns:
            str: ПІБ пацієнта, ім'я користувача або порожній рядок.
        """
        if self.last_name or self.first_name:
            return self.full_name

        if self.user:
            return self.user.full_name or self.user.username

        return ""

    @property
    def full_name(self) -> str:
        """
        Повертає ПІБ пацієнта.

        Returns:
            str: Повне ім'я пацієнта.
        """
        return " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))

    @property
    def appointment_end_time(self):
        """
        Повертає час завершення слота.

        Returns:
            object: Час завершення прийому або None.
        """
        workday = DoctorWorkDay.objects.filter(
            doctor=self.doctor,
            direction=self.direction,
            work_date=self.appointment_date,
        ).first()

        if not workday:
            return None

        start_dt = datetime.combine(self.appointment_date, self.appointment_time)
        end_dt = start_dt + timedelta(minutes=workday.appointment_duration_minutes)
        return end_dt.time()

    @property
    def appointment_time_range(self) -> str:
        """
        Повертає часовий діапазон слота.

        Returns:
            str: Діапазон часу у форматі HH:MM - HH:MM або тільки час початку.
        """
        end_time = self.appointment_end_time
        start_str = self.appointment_time.strftime("%H:%M")

        if not end_time:
            return start_str

        return f"{start_str} - {end_time.strftime('%H:%M')}"

    def __str__(self) -> str:
        """
        Повертає строкове представлення запису.

        Returns:
            str: Опис запису з пацієнтом, лікарем, датою та часом.
        """
        return (
            f"{self.customer_name} — {self.doctor.full_name} — "
            f"{self.appointment_date} {self.appointment_time_range}"
        )
