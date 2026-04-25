from __future__ import annotations

from django.db import models


class Analysis(models.Model):
    """
    Модель лабораторного аналізу.

    Зберігає основну інформацію про аналіз, його категорії,
    термін виконання та вартість.
    """

    name: models.CharField = models.CharField(
        max_length=255,
        verbose_name="Назва аналізу",
    )
    what_to_check: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Що перевірити",
    )
    disease: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Захворювання",
    )
    for_whom: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Для кого",
    )
    biomaterial: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Біоматеріал",
    )
    duration_days: models.PositiveIntegerField = models.PositiveIntegerField(
        verbose_name="Термін виконання (днів)",
    )
    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Ціна",
    )
    is_active: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Активний",
    )

    class Meta:
        """
        Метадані моделі аналізу.
        """

        verbose_name = "Аналіз"
        verbose_name_plural = "Аналізи"
        ordering = ["name"]

    def __str__(self) -> str:
        """
        Повертає строкове представлення аналізу.

        Returns:
            str: Назва аналізу.
        """
        return str(self.name)