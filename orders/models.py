from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models

from analysis.models import Analysis


class OrderStatus(models.TextChoices):
    """
    Перелік статусів замовлення аналізів.
    """

    NEW = "new", "Нове"
    COMPLETED = "completed", "Завершено"
    REJECTED = "rejected", "Відхилено"


class Order(models.Model):
    """
    Модель замовлення аналізів.

    Зберігає основну інформацію про замовлення користувача:
    дату створення, статус, загальну суму та файл із результатами.
    """

    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Користувач",
    )
    status: models.CharField = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        verbose_name="Статус",
    )
    total_price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Загальна сума",
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення",
    )
    result_file: models.FileField = models.FileField(
        upload_to="orders/results/",
        blank=True,
        null=True,
        verbose_name="Результати аналізів (PDF)",
    )

    class Meta:
        """
        Метадані моделі замовлення.
        """

        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        Повертає строкове представлення замовлення.

        Returns:
            str: Рядок з ідентифікатором замовлення.
        """
        return f"Замовлення #{self.id}"

    @property
    def analyses_count(self) -> int:
        """
        Повертає кількість аналізів у замовленні.

        Returns:
            int: Кількість елементів замовлення.
        """
        return self.items.count()


class OrderItem(models.Model):
    """
    Модель елемента замовлення.

    Зберігає конкретний аналіз, його ціну на момент оформлення
    та зв'язок із замовленням.
    """

    order: models.ForeignKey = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Замовлення",
    )
    analysis: models.ForeignKey = models.ForeignKey(
        Analysis,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="Аналіз",
    )
    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Ціна",
    )

    class Meta:
        """
        Метадані моделі елемента замовлення.
        """

        verbose_name = "Елемент замовлення"
        verbose_name_plural = "Елементи замовлення"

    def __str__(self) -> str:
        """
        Повертає строкове представлення елемента замовлення.

        Returns:
            str: Рядок із назвою аналізу.
        """
        return f"{self.analysis.name} — {self.order}"