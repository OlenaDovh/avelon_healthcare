from __future__ import annotations
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from analysis.models import Analysis


class OrderStatus(models.TextChoices):
    """
    Перелік статусів замовлення аналізів.
    """

    NEW = "new", "Нове"
    PAID = "paid", "Сплачено"
    COMPLETED = "completed", "Завершено"
    REJECTED = "rejected", "Відхилено"


class PaymentMethod(models.TextChoices):
    """
    Перелік способів оплати.
    """

    ONLINE = "online", "Онлайн"
    BANK_TRANSFER = "bank_transfer", "На рахунок"
    CASH = "cash", "На касі"


class Order(models.Model):
    """
    Модель замовлення аналізів.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Користувач",
        blank=True,
        null=True,
    )

    last_name = models.CharField(max_length=150, blank=True, default="", verbose_name="Прізвище")
    first_name = models.CharField(max_length=150, blank=True, default="", verbose_name="Ім'я")
    middle_name = models.CharField(max_length=150, blank=True, default="", verbose_name="По батькові")

    phone = models.CharField(max_length=30, blank=True, default="", verbose_name="Телефон")
    email = models.EmailField(blank=True, default="", verbose_name="Email")

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        verbose_name="Статус",
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        verbose_name="Спосіб оплати",
    )

    paid_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата оплати")

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Загальна сума",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    result_file = models.FileField(
        upload_to="orders/results/",
        blank=True,
        null=True,
        verbose_name="Результати аналізів (PDF)",
    )

    rejection_reason = models.TextField(blank=True, verbose_name="Причина відхилення")

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Замовлення #{self.id}"

    def clean(self) -> None:
        """
        Валідація моделі.
        """
        if self.status == OrderStatus.REJECTED and not self.rejection_reason.strip():
            raise ValidationError(
                {"rejection_reason": "Вкажіть причину відхилення."}
            )

    @property
    def analyses_count(self) -> int:
        """Кількість аналізів у замовленні."""
        return self.items.count()

    @property
    def customer_name(self) -> str:
        """
        Повертає ім'я замовника (пріоритет: введені дані → user).
        """
        if self.last_name or self.first_name:
            return self.full_name

        if self.user:
            return self.user.full_name or self.user.username

        return ""

    @property
    def full_name(self) -> str:
        """ПІБ замовника."""
        return " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))

    def mark_as_paid(self) -> None:
        """
        Позначає замовлення як сплачене.
        """
        self.status = OrderStatus.PAID
        self.paid_at = timezone.now()
        self.save(update_fields=["status", "paid_at"])


class OrderItem(models.Model):
    """
    Модель елемента замовлення.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Замовлення",
    )

    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="Аналіз",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Ціна",
    )

    class Meta:
        verbose_name = "Елемент замовлення"
        verbose_name_plural = "Елементи замовлення"

    def __str__(self) -> str:
        return f"{self.analysis.name} — {self.order}"
