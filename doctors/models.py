from __future__ import annotations

from django.db import models


class Direction(models.Model):
    """
    Модель медичного напряму клініки.

    Використовується для групування лікарів за спеціалізаціями
    та відображення інформації про медичні послуги.
    """

    name: models.CharField = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Назва напряму",
    )
    description: models.TextField = models.TextField(
        verbose_name="Опис напряму",
    )

    class Meta:
        """
        Метадані моделі напряму.
        """

        verbose_name = "Напрям"
        verbose_name_plural = "Напрями"
        ordering = ["name"]

    def __str__(self) -> str:
        """
        Повертає строкове представлення напряму.

        Returns:
            str: Назва напряму.
        """
        return str(self.name)


class Doctor(models.Model):
    """
    Модель лікаря клініки.

    Зберігає базову інформацію про лікаря, його спеціальність,
    категорію, стаж, фото та напрями, з якими він працює.
    """

    full_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name="ПІБ лікаря",
    )
    position: models.CharField = models.CharField(
        max_length=255,
        verbose_name="Посада",
    )
    specialty_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name="Назва спеціальності",
    )
    qualification_category: models.CharField = models.CharField(
        max_length=255,
        verbose_name="Кваліфікаційна категорія",
    )
    experience_years: models.PositiveIntegerField = models.PositiveIntegerField(
        verbose_name="Стаж (років)",
    )
    price_from: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Ціна від",
    )
    price_to: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Ціна до",
    )
    photo: models.ImageField = models.ImageField(
        upload_to="doctors/photos/",
        blank=True,
        null=True,
        verbose_name="Фото",
    )
    work_experience_description: models.TextField = models.TextField(
        blank=True,
        verbose_name="Досвід роботи",
    )
    when_to_contact: models.TextField = models.TextField(
        blank=True,
        verbose_name="У яких випадках звертатись",
    )
    education: models.TextField = models.TextField(
        blank=True,
        verbose_name="Освіта",
    )
    licenses: models.ImageField = models.ImageField(
        upload_to="doctors/licenses/",
        blank=True,
        null=True,
        verbose_name="Ліцензії / фото ліцензій",
    )
    directions: models.ManyToManyField = models.ManyToManyField(
        Direction,
        related_name="doctors",
        verbose_name="Напрями",
    )

    class Meta:
        """
        Метадані моделі лікаря.
        """

        verbose_name = "Лікар"
        verbose_name_plural = "Лікарі"
        ordering = ["full_name"]

    def __str__(self) -> str:
        """
        Повертає строкове представлення лікаря.

        Returns:
            str: ПІБ лікаря.
        """
        return str(self.full_name)