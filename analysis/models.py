"""Модуль analysis/models.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.db import models

class Analysis(models.Model):
    """Клас Analysis.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    name: models.CharField = models.CharField(max_length=255, verbose_name='Назва аналізу')
    what_to_check: models.CharField = models.CharField(max_length=255, blank=True, verbose_name='Що перевірити')
    disease: models.CharField = models.CharField(max_length=255, blank=True, verbose_name='Захворювання')
    for_whom: models.CharField = models.CharField(max_length=255, blank=True, verbose_name='Для кого')
    biomaterial: models.CharField = models.CharField(max_length=255, blank=True, verbose_name='Біоматеріал')
    duration_days: models.PositiveIntegerField = models.PositiveIntegerField(verbose_name='Термін виконання (днів)')
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    is_active: models.BooleanField = models.BooleanField(default=True, verbose_name='Активний')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Аналіз'
        verbose_name_plural = 'Аналізи'
        ordering = ['name']

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return str(self.name)
