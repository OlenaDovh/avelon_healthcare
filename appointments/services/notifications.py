"""Модуль `appointments/services/notifications.py` застосунку `appointments`.

Містить код проєкту Avelon Healthcare та відповідає за частину бізнес-логіки, налаштувань, форм, моделей, представлень або допоміжних сервісів.
Документація в модулі додана українською мовою для полегшення підтримки, читання коду та генерації технічної документації.
"""

from __future__ import annotations

from django.template.loader import render_to_string

from core.utils.email import send_html_email
from appointments.models import Appointment


def send_appointment_email(appointment: Appointment) -> None:
    """Виконує прикладну логіку функції `send_appointment_email` у відповідному модулі проєкту.

    Параметри:
        appointment: Значення типу `Appointment`, яке передається для виконання логіки функції.

    Повертає:
        None: Функція виконує дію без явного значення результату.
    """
    html_body = render_to_string(
        "avelon_healthcare/appointments/email/appointment_email.html",
        {
            "appointment": appointment,
        },
    )

    send_html_email(
        subject=f"Avelon Healthcare — запис до лікаря #{appointment.id}",
        html_body=html_body,
        to=[appointment.email],
    )
