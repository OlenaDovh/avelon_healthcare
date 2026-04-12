from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from doctors.models import Direction, Doctor


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
    """

    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Користувач",
        blank=True,
        null=True,
    )
    full_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name="ПІБ",
        blank=True,
        default="",
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
            ValidationError: Якщо лікар не належить до вибраного напряму.
        """
        if self.doctor_id and self.direction_id:
            if not self.doctor.directions.filter(id=self.direction_id).exists():
                raise ValidationError(
                    {"doctor": "Обраний лікар не працює в цьому напрямі."}
                )

    @property
    def customer_name(self) -> str:
        """
        Повертає ім'я пацієнта.

        Returns:
            str: Ім'я пацієнта.
        """
        if self.full_name:
            return self.full_name

        if self.user:
            return self.user.get_full_name() or self.user.username

        return ""

    def __str__(self) -> str:
        """
        Повертає строкове представлення запису.

        Returns:
            str: Інформація про запис.
        """
        return (
            f"{self.customer_name} — {self.doctor.full_name} — "
            f"{self.appointment_date} {self.appointment_time}"
        )