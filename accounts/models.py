from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r"^\+380\d{9}$",
    message="Номер телефону має бути у форматі +380XXXXXXXXX",
)


class PreferredContactChannel(models.TextChoices):
    PHONE = "phone", "Телефон"
    EMAIL = "email", "Email"
    TELEGRAM = "telegram", "Telegram"
    VIBER = "viber", "Viber"


class User(AbstractUser):
    """
    Кастомна модель користувача.

    Розширює стандартну модель користувача додатковими полями та логікою валідації.
    """

    first_name = models.CharField(max_length=150, verbose_name="Ім'я")
    last_name = models.CharField(max_length=150, verbose_name="Прізвище")
    middle_name = models.CharField(max_length=150, blank=True, verbose_name="По батькові")

    email = models.EmailField(
        unique=True,
        verbose_name="Електронна пошта",
    )

    pending_email = models.EmailField(
        blank=True,
        default="",
        verbose_name="Нова електронна пошта (очікує підтвердження)",
    )

    phone = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        validators=[phone_validator],
        verbose_name="Номер телефону",
    )

    email_verified = models.BooleanField(
        default=False,
        verbose_name="Пошта підтверджена",
    )

    discount = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Знижка, %",
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата народження",
    )

    preferred_contact_channel = models.CharField(
        max_length=20,
        choices=PreferredContactChannel.choices,
        blank=True,
        verbose_name="Пріоритетний канал зв’язку",
    )

    def clean(self) -> None:
        """
        Виконує валідацію моделі користувача.

        Raises:
            ValidationError: Якщо телефон не вказаний для не-суперкористувача.
        """
        super().clean()

        if not self.is_superuser and not self.phone:
            raise ValidationError({"phone": "Телефон обовʼязковий для користувача."})

    def save(self, *args, **kwargs) -> None:
        """
        Зберігає користувача з додатковою логікою обробки полів.

        Args:
            *args: Позиційні аргументи.
            **kwargs: Іменовані аргументи.

        Returns:
            None
        """
        if not self.phone:
            self.phone = None

        if self.is_superuser and self.email:
            self.email_verified = True
            self.pending_email = ""

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Повертає рядкове представлення користувача.

        Returns:
            str: Повне ім'я або username.
        """
        return self.full_name or self.username

    @property
    def full_name(self) -> str:
        """
        Повертає повне ім'я користувача.

        Returns:
            str: Конкатенація прізвища, імені та по батькові.
        """
        return " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))
