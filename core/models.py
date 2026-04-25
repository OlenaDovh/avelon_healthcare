"""Модуль core/models.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import models

class ClinicInfo(models.Model):
    """Клас ClinicInfo.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    title: models.CharField = models.CharField(max_length=255, verbose_name='Заголовок')
    description: models.TextField = models.TextField(verbose_name='Опис')
    goals: models.TextField = models.TextField(blank=True, verbose_name='Цілі')
    values: models.TextField = models.TextField(blank=True, verbose_name='Цінності')
    achievements: models.TextField = models.TextField(blank=True, verbose_name='Досягнення')
    image: models.ImageField = models.ImageField(upload_to='core/clinic/', blank=True, null=True, verbose_name='Фото')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Інформація про клініку'
        verbose_name_plural = 'Інформація про клініку'

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return str(self.title)

class ContactInfo(models.Model):
    """Клас ContactInfo.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    address: models.CharField = models.CharField(max_length=255, verbose_name='Адреса')
    work_schedule: models.CharField = models.CharField(max_length=255, verbose_name='Графік роботи')
    phone_1: models.CharField = models.CharField(max_length=20, verbose_name='Телефон 1')
    phone_2: models.CharField = models.CharField(max_length=20, blank=True, verbose_name='Телефон 2')
    email: models.EmailField = models.EmailField(verbose_name='Email')
    google_map_embed_url = models.TextField(blank=True, verbose_name='Google Maps Embed URL')
    facebook_url: models.URLField = models.URLField(blank=True, verbose_name='Facebook')
    instagram_url: models.URLField = models.URLField(blank=True, verbose_name='Instagram')
    youtube_url: models.URLField = models.URLField(blank=True, verbose_name='YouTube')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Контакти'
        verbose_name_plural = 'Контакти'

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return 'Контактна інформація клініки'

class Promotion(models.Model):
    """Клас Promotion.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    title: models.CharField = models.CharField(max_length=255, verbose_name='Назва акції')
    image: models.ImageField = models.ImageField(upload_to='core/promotions/', blank=True, null=True, verbose_name='Фото')
    description: models.TextField = models.TextField(verbose_name='Опис')
    end_date: models.DateField = models.DateField(verbose_name='Термін дії до')
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Акція'
        verbose_name_plural = 'Акції'
        ordering = ['-end_date']

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return str(self.title)
