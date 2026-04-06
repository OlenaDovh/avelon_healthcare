from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from appointments.models import Appointment, AppointmentStatus


BAD_WORDS: list[str] = [
    "дурак",
    "дурень",
    "ідіот",
    "тупий",
    "лайно",
]


class Review(models.Model):
    """
    Модель відгуку користувача.

    Відгук може бути пов'язаний із конкретним завершеним прийомом.
    Представник клініки може додати відповідь через адмінку.
    """

    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Користувач",
    )
    appointment: models.OneToOneField = models.OneToOneField(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review",
        verbose_name="Запис до лікаря",
    )
    text: models.TextField = models.TextField(
        verbose_name="Текст відгуку",
    )
    clinic_reply: models.TextField = models.TextField(
        blank=True,
        verbose_name="Відповідь представника клініки",
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення",
    )

    class Meta:
        """
        Метадані моделі відгуку.
        """

        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["-created_at"]

    def clean(self) -> None:
        """
        Перевіряє коректність відгуку.

        Raises:
            ValidationError: Якщо в тексті є небажані слова або
            якщо запис не належить користувачу / не завершений.
        """
        lowered_text: str = self.text.lower()

        for bad_word in BAD_WORDS:
            if bad_word in lowered_text:
                raise ValidationError(
                    {"text": "Відгук містить небажану лексику."}
                )

        if self.appointment:
            if self.appointment.user_id != self.user_id:
                raise ValidationError(
                    {"appointment": "Цей запис не належить поточному користувачу."}
                )

            if self.appointment.status != AppointmentStatus.COMPLETED:
                raise ValidationError(
                    {"appointment": "Відгук можна залишити лише для завершеного прийому."}
                )

    def __str__(self) -> str:
        """
        Повертає строкове представлення відгуку.

        Returns:
            str: Рядок із користувачем і датою створення.
        """
        return f"Відгук від {self.user.username} ({self.created_at:%d.%m.%Y})"
