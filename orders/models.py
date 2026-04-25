"""Модуль orders/models.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from analysis.models import Analysis

class OrderStatus(models.TextChoices):
    """Клас OrderStatus.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    NEW = ('new', 'Нове')
    PAID = ('paid', 'Сплачено')
    COMPLETED = ('completed', 'Завершено')
    REJECTED = ('rejected', 'Відхилено')

class PaymentMethod(models.TextChoices):
    """Клас PaymentMethod.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    ONLINE = ('online', 'Онлайн')
    BANK_TRANSFER = ('bank_transfer', 'На рахунок')
    CASH = ('cash', 'На касі')

class Order(models.Model):
    """Клас Order.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name='Користувач', blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, default='', verbose_name='Прізвище')
    first_name = models.CharField(max_length=150, blank=True, default='', verbose_name="Ім'я")
    middle_name = models.CharField(max_length=150, blank=True, default='', verbose_name='По батькові')
    phone: models.CharField = models.CharField(max_length=30, verbose_name='Телефон', blank=True, default='')
    email: models.EmailField = models.EmailField(verbose_name='Email', blank=True, default='')
    status: models.CharField = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.NEW, verbose_name='Статус')
    payment_method: models.CharField = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.CASH, verbose_name='Спосіб оплати')
    paid_at: models.DateTimeField = models.DateTimeField(blank=True, null=True, verbose_name='Дата оплати')
    total_price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Загальна сума')
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    result_file: models.FileField = models.FileField(upload_to='orders/results/', blank=True, null=True, verbose_name='Результати аналізів (PDF)')
    rejection_reason: models.TextField = models.TextField(blank=True, verbose_name='Причина відхилення')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return f'Замовлення #{self.id}'

    def clean(self) -> None:
        """Виконує логіку `clean`.

Returns:
    None."""
        if self.status == OrderStatus.REJECTED and (not self.rejection_reason.strip()):
            raise ValidationError({'rejection_reason': 'Вкажіть причину відхилення.'})

    @property
    def analyses_count(self) -> int:
        """Виконує логіку `analyses_count`.

Returns:
    Результат виконання операції."""
        return self.items.count()

    @property
    def customer_name(self) -> str:
        """Виконує логіку `customer_name`.

Returns:
    Результат виконання операції."""
        if self.last_name or self.first_name:
            return self.full_name
        if self.user:
            return self.user.full_name or self.user.username
        return ''

    def mark_as_paid(self) -> None:
        """Виконує логіку `mark_as_paid`.

Returns:
    None."""
        self.status = OrderStatus.PAID
        self.paid_at = timezone.now()
        self.save(update_fields=['status', 'paid_at'])

    @property
    def full_name(self) -> str:
        """Виконує логіку `full_name`.

Returns:
    Результат виконання операції."""
        return ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))

class OrderItem(models.Model):
    """Клас OrderItem.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
    order: models.ForeignKey = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Замовлення')
    analysis: models.ForeignKey = models.ForeignKey(Analysis, on_delete=models.PROTECT, related_name='order_items', verbose_name='Аналіз')
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')

    class Meta:
        """Клас Meta.

Відповідає за поведінку, описану в цьому компоненті застосунку."""
        verbose_name = 'Елемент замовлення'
        verbose_name_plural = 'Елементи замовлення'

    def __str__(self) -> str:
        """Виконує логіку `__str__`.

Returns:
    Результат виконання операції."""
        return f'{self.analysis.name} — {self.order}'
