from django.db import transaction
from appointments.models import Appointment
from appointments.tasks import send_appointment_email_task


def fill_appointment_from_user(*, appointment: Appointment, user) -> Appointment:
    """
    Заповнює дані запису на прийом даними користувача.

    Args:
        appointment: Запис на прийом.
        user: Користувач, даними якого заповнюється запис.

    Returns:
        Appointment: Оновлений запис на прийом.
    """
    appointment.user = user
    appointment.last_name = user.last_name
    appointment.first_name = user.first_name
    appointment.middle_name = getattr(user, "middle_name", "") or ""
    appointment.phone = getattr(user, "phone", "") or ""
    appointment.email = user.email or ""
    return appointment


def fill_appointment_from_guest_data(*, appointment: Appointment, cleaned_data: dict) -> Appointment:
    """
    Заповнює дані запису на прийом даними незареєстрованого пацієнта.

    Args:
        appointment: Запис на прийом.
        cleaned_data: Очищені дані форми.

    Returns:
        Appointment: Оновлений запис на прийом.
    """
    appointment.user = None
    appointment.last_name = cleaned_data["last_name"]
    appointment.first_name = cleaned_data["first_name"]
    appointment.middle_name = cleaned_data.get("middle_name", "")
    appointment.phone = cleaned_data["phone"]
    appointment.email = cleaned_data["email"]
    return appointment


def save_new_appointment(*, appointment: Appointment) -> Appointment:
    """
    Зберігає новий запис на прийом і планує надсилання email.

    Args:
        appointment: Запис на прийом для збереження.

    Returns:
        Appointment: Збережений запис на прийом.
    """
    appointment.save()

    transaction.on_commit(
        lambda: send_appointment_email_task.delay(appointment.id)
    )

    return appointment
