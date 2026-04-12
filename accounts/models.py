from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


phone_validator: RegexValidator = RegexValidator(
    regex=r'^\+380\d{9}$',
    message='Номер телефону має бути у форматі +380XXXXXXXXX'
)


class User(AbstractUser):
    """
    Кастомна модель користувача.

    Розширює стандартну модель Django, додаючи:
    - номер телефону
    - статус підтвердження email
    - знижку
    - дату народження
    - пріоритетний канал зв’язку
    """

    first_name = models.CharField(max_length=150, verbose_name="Ім'я")
    last_name = models.CharField(max_length=150, verbose_name="Прізвище")
    middle_name = models.CharField(max_length=150, blank=True, verbose_name="По батькові")

    email = models.EmailField(
        unique=True,
        verbose_name='Електронна пошта'
    )

    phone = models.CharField(
        max_length=13,
        unique=True,
        validators=[phone_validator],
        verbose_name='Номер телефону'
    )

    email_verified: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name='Пошта підтверджена'
    )

    discount: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        verbose_name='Знижка, %'
    )

    birth_date: models.DateField = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата народження'
    )

    CONTACT_CHOICES: list[tuple[str, str]] = [
        ('phone', 'Телефон'),
        ('email', 'Email'),
        ('telegram', 'Telegram'),
        ('viber', 'Viber'),
    ]

    preferred_contact_channel: models.CharField = models.CharField(
        max_length=20,
        choices=CONTACT_CHOICES,
        blank=True,
        verbose_name='Пріоритетний канал зв’язку'
    )

    def __str__(self) -> str:
        """
        Повертає строкове представлення користувача.

        Returns:
            str: Логін користувача
        """
        return self.username